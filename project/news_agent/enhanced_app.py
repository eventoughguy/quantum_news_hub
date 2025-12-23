from flask import Flask, render_template, jsonify
import sqlite3
import logging
import sys
import os
from pathlib import Path
from datetime import datetime

# Add ontology module to path
ontology_path = Path(__file__).parent.parent / "ontology"
sys.path.append(str(ontology_path))

try:
    from rdflib import Graph, Namespace
    from quantum_supply_chain_ontology import QuantumSupplyChainOntology
    ONTOLOGY_AVAILABLE = True
except ImportError:
    ONTOLOGY_AVAILABLE = False
    logging.warning("Ontology modules not available")

app = Flask(__name__)

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

class QuantumNewsDB:
    def __init__(self, db_path="quantum_news_rss.db"):
        self.db_path = db_path

    def get_all_articles(self, limit=20):
        """Get all articles with summaries, ordered by most recent"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute("""
            SELECT id, title, author, publish_date, article_link, ai_summary, created_at
            FROM quantum_news_rss
            WHERE ai_summary IS NOT NULL AND ai_summary != ''
            ORDER BY created_at DESC
            LIMIT ?
        """, (limit,))

        articles = cursor.fetchall()
        conn.close()

        # Format articles as dictionaries
        formatted_articles = []
        for article in articles:
            formatted_articles.append({
                'id': article[0],
                'title': article[1],
                'author': article[2] or 'Unknown Author',
                'publish_date': article[3],
                'link': article[4],
                'summary': article[5],
                'created_at': article[6]
            })

        return formatted_articles

    def get_article_stats(self):
        """Get statistics about articles"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # Total articles
        cursor.execute("SELECT COUNT(*) FROM quantum_news_rss")
        total_articles = cursor.fetchone()[0]

        # Articles with summaries
        cursor.execute("SELECT COUNT(*) FROM quantum_news_rss WHERE ai_summary IS NOT NULL AND ai_summary != ''")
        articles_with_summary = cursor.fetchone()[0]

        # Articles without summaries
        articles_without_summary = total_articles - articles_with_summary

        # Most recent article date
        cursor.execute("SELECT MAX(created_at) FROM quantum_news_rss")
        last_updated = cursor.fetchone()[0]

        conn.close()

        return {
            'total_articles': total_articles,
            'articles_with_summary': articles_with_summary,
            'articles_without_summary': articles_without_summary,
            'last_updated': last_updated
        }

class OntologyVisualizer:
    """Handles ontology data for visualization"""

    def __init__(self):
        self.ontology_file = ontology_path / "quantum_supply_chain_ontology.ttl"

        #self.ontology_file = ontology_path / "quantum_info.ttl"
        self.graph = None
        self.qsc_namespace = Namespace("http://quantum-supply-chain.org/ontology#")

    def load_ontology(self):
        """Load the ontology file"""
        if not ONTOLOGY_AVAILABLE:
            return False

        try:
            self.graph = Graph()
            if self.ontology_file.exists():
                self.graph.parse(str(self.ontology_file), format="ttl")
                return True
            return False
        except Exception as e:
            logging.error(f"Error loading ontology: {e}")
            return False

    def normalize_name_for_id(self, name):
        """Convert company name to consistent ID format"""
        return str(name).replace(' ', '_').replace('.', '').replace(',', '').replace('(', '').replace(')', '').replace('-', '_')

    def get_visualization_data(self):
        """Get data formatted for D3.js visualization"""
        if not self.graph:
            if not self.load_ontology():
                return {'nodes': [], 'links': []}

        nodes = []
        links = []
        node_ids = set()

        try:
            # Get hardware companies
            hw_companies = self.get_companies_by_type("QuantumHardwareCompany")
            for company in hw_companies:
                node_id = f"hw_{self.normalize_name_for_id(company['name'])}"
                nodes.append({
                    'id': node_id,
                    'name': company['name'],
                    'type': 'hardware',
                    'group': 1,
                    'details': company
                })
                node_ids.add(node_id)

            # Get component suppliers
            suppliers = self.get_companies_by_type("ComponentSupplier")
            for supplier in suppliers:
                node_id = f"sup_{self.normalize_name_for_id(supplier['name'])}"
                nodes.append({
                    'id': node_id,
                    'name': supplier['name'],
                    'type': 'supplier',
                    'group': 2,
                    'details': supplier
                })
                node_ids.add(node_id)

            # Get software companies
            software = self.get_companies_by_type("SoftwareCompany")
            for sw in software:
                node_id = f"sw_{self.normalize_name_for_id(sw['name'])}"
                nodes.append({
                    'id': node_id,
                    'name': sw['name'],
                    'type': 'software',
                    'group': 3,
                    'details': sw
                })
                node_ids.add(node_id)

            # Create links based on relationships, but only for nodes that exist
            links.extend(self.get_supply_relationships(node_ids))
            links.extend(self.get_software_relationships(node_ids))

            return {'nodes': nodes, 'links': links}

        except Exception as e:
            logging.error(f"Error generating visualization data: {e}")
            return {'nodes': [], 'links': []}

    def get_companies_by_type(self, company_type):
        """Get companies of a specific type"""
        companies = []

        query = f"""
        PREFIX qsc: <http://quantum-supply-chain.org/ontology#>
        SELECT ?company ?name ?country ?website ?notes WHERE {{
            ?company a qsc:{company_type} .
            ?company qsc:name ?name .
            OPTIONAL {{ ?company qsc:country ?country }}
            OPTIONAL {{ ?company qsc:website ?website }}
            OPTIONAL {{ ?company qsc:notes ?notes }}
        }}
        """

        results = self.graph.query(query)
        for row in results:
            companies.append({
                'uri': str(row[0]),
                'name': str(row[1]),
                'country': str(row[2]) if row[2] else '',
                'website': str(row[3]) if row[3] else '',
                'notes': str(row[4]) if row[4] else '',
                'type': company_type
            })

        return companies

    def get_supply_relationships(self, valid_node_ids):
        """Get supplier-client relationships"""
        links = []

        query = """
        PREFIX qsc: <http://quantum-supply-chain.org/ontology#>
        SELECT ?supplier ?supplierName ?client ?clientName WHERE {
            ?supplier qsc:hasClient ?client .
            ?supplier qsc:name ?supplierName .
            ?client qsc:name ?clientName .
        }
        """

        results = self.graph.query(query)
        for row in results:
            supplier_id = f"sup_{self.normalize_name_for_id(str(row[1]))}"
            client_id = f"hw_{self.normalize_name_for_id(str(row[3]))}"

            # Only create links for nodes that actually exist
            if supplier_id in valid_node_ids and client_id in valid_node_ids:
                links.append({
                    'source': supplier_id,
                    'target': client_id,
                    'type': 'supplies',
                    'strength': 1
                })

        return links

    def get_software_relationships(self, valid_node_ids):
        """Get software-hardware relationships"""
        links = []

        query = """
        PREFIX qsc: <http://quantum-supply-chain.org/ontology#>
        SELECT ?software ?softwareName ?hardware ?hardwareName WHERE {
            ?software qsc:supportsHardware ?hardware .
            ?software qsc:name ?softwareName .
            ?hardware qsc:name ?hardwareName .
        }
        """

        results = self.graph.query(query)
        for row in results:
            software_id = f"sw_{self.normalize_name_for_id(str(row[1]))}"
            hardware_id = f"hw_{self.normalize_name_for_id(str(row[3]))}"

            # Only create links for nodes that actually exist
            if software_id in valid_node_ids and hardware_id in valid_node_ids:
                links.append({
                    'source': software_id,
                    'target': hardware_id,
                    'type': 'supports',
                    'strength': 0.8
                })

        return links

    def get_node_details(self, node_id):
        """Get detailed information for a specific node"""
        if not self.graph:
            if not self.load_ontology():
                return {}

        # Extract name from node_id (remove type prefix)
        name = node_id.split('_', 1)[1] if '_' in node_id else node_id

        query = f"""
        PREFIX qsc: <http://quantum-supply-chain.org/ontology#>
        SELECT ?prop ?value WHERE {{
            ?company qsc:name "{name}" .
            ?company ?prop ?value .
        }}
        """

        details = {'name': name}
        results = self.graph.query(query)
        for row in results:
            prop = str(row[0]).split('#')[-1]  # Get property name after #
            value = str(row[1])
            details[prop] = value

        return details

db = QuantumNewsDB()
ontology_viz = OntologyVisualizer() if ONTOLOGY_AVAILABLE else None

@app.route("/")
def index():
    """Render the main page with ontology integration"""
    return render_template("quantum_hub_with_ontology.html")

@app.route("/api/articles")
def get_articles():
    """API endpoint to get all articles"""
    try:
        articles = db.get_all_articles()
        return jsonify({
            'status': 'success',
            'articles': articles,
            'count': len(articles)
        })
    except Exception as e:
        logging.error(f"Error fetching articles: {e}")
        return jsonify({
            'status': 'error',
            'message': 'Failed to fetch articles'
        }), 500

@app.route("/api/stats")
def get_stats():
    """API endpoint to get article statistics"""
    try:
        stats = db.get_article_stats()
        return jsonify({
            'status': 'success',
            'stats': stats
        })
    except Exception as e:
        logging.error(f"Error fetching stats: {e}")
        return jsonify({
            'status': 'error',
            'message': 'Failed to fetch statistics'
        }), 500

@app.route("/api/health")
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat()
    })

# Ontology API endpoints
@app.route("/api/ontology/graph")
def get_ontology_graph():
    """Get ontology data for visualization"""
    if not ontology_viz:
        return jsonify({
            'status': 'error',
            'message': 'Ontology visualization not available'
        }), 503

    try:
        graph_data = ontology_viz.get_visualization_data()
        return jsonify({
            'status': 'success',
            'data': graph_data
        })
    except Exception as e:
        logging.error(f"Error generating ontology graph: {e}")
        return jsonify({
            'status': 'error',
            'message': 'Failed to generate ontology graph'
        }), 500

@app.route("/api/ontology/node/<node_id>")
def get_node_details(node_id):
    """Get detailed information for a specific node"""
    if not ontology_viz:
        return jsonify({
            'status': 'error',
            'message': 'Ontology visualization not available'
        }), 503

    try:
        details = ontology_viz.get_node_details(node_id)
        return jsonify({
            'status': 'success',
            'details': details
        })
    except Exception as e:
        logging.error(f"Error getting node details: {e}")
        return jsonify({
            'status': 'error',
            'message': 'Failed to get node details'
        }), 500

# Legacy endpoint for backward compatibility
@app.route("/get_news")
def get_news_legacy():
    """Legacy endpoint for backward compatibility"""
    try:
        articles = db.get_all_articles()
        # Transform to match old format
        legacy_format = []
        for article in articles:
            legacy_format.append([
                article['title'],
                article['link'],
                article['summary'],
                article['publish_date']
            ])
        return jsonify(legacy_format)
    except Exception as e:
        logging.error(f"Error in legacy endpoint: {e}")
        return jsonify([])

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5001)