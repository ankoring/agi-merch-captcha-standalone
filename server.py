#!/usr/bin/env python3
"""
AGI House Merch CAPTCHA - Simple Python Server Demo
Simulates the Node.js backend functionality
"""

import json
import random
import uuid
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
import time

class AGICaptchaHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        """Handle GET requests"""
        if self.path == '/':
            self.serve_html()
        elif self.path == '/health':
            self.serve_health()
        else:
            self.send_error(404)
    
    def do_POST(self):
        """Handle POST requests"""
        if self.path == '/api/generate-captcha':
            self.generate_captcha()
        elif self.path == '/api/verify-captcha':
            self.verify_captcha()
        else:
            self.send_error(404)
    
    def serve_html(self):
        """Serve the main HTML file"""
        try:
            with open('index.html', 'r', encoding='utf-8') as f:
                content = f.read()
            
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(content.encode('utf-8'))
        except FileNotFoundError:
            self.send_error(404)
    
    def serve_health(self):
        """Health check endpoint"""
        response = {
            "status": "healthy",
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "service": "AGI House CAPTCHA Demo",
            "version": "1.0.0"
        }
        
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(response).encode('utf-8'))
    
    def generate_captcha(self):
        """Generate a new CAPTCHA challenge"""
        # AGI House merch images
        agi_merch = [
            {"id": 1, "url": "/images/neural-tshirt.jpg", "alt": "Neural Network T-Shirt", "description": "AI-themed t-shirt with neural network design"},
            {"id": 2, "url": "/images/quantum-hoodie.jpg", "alt": "Quantum Computing Hoodie", "description": "Quantum computing themed hoodie"},
            {"id": 3, "url": "/images/ai-cap.jpg", "alt": "AI Cap", "description": "Baseball cap with AGI House AI logo"},
            {"id": 4, "url": "/images/future-mug.jpg", "alt": "Future Mug", "description": "Ceramic mug with futuristic AI design"},
            {"id": 5, "url": "/images/agi-stickers.jpg", "alt": "AGI Sticker Pack", "description": "Collection of AGI House branded stickers"},
            {"id": 6, "url": "/images/neural-tote.jpg", "alt": "Neural Tote Bag", "description": "Canvas tote bag with AGI House branding"}
        ]
        
        # Distractor images
        distractors = [
            {"id": 7, "url": "/images/plain-tshirt.jpg", "alt": "Plain T-Shirt", "description": "Basic white cotton t-shirt"},
            {"id": 8, "url": "/images/generic-hoodie.jpg", "alt": "Generic Hoodie", "description": "Plain black hoodie without branding"},
            {"id": 9, "url": "/images/basic-cap.jpg", "alt": "Basic Cap", "description": "Simple baseball cap"},
            {"id": 10, "url": "/images/coffee-mug.jpg", "alt": "Coffee Mug", "description": "Plain ceramic coffee mug"},
            {"id": 11, "url": "/images/notebook.jpg", "alt": "Notebook", "description": "Basic spiral notebook"},
            {"id": 12, "url": "/images/water-bottle.jpg", "alt": "Water Bottle", "description": "Generic water bottle"}
        ]
        
        # Create 3x3 grid (9 images total)
        all_images = agi_merch + distractors
        random.shuffle(all_images)
        grid = all_images[:9]
        
        # Select 3-4 AGI merch images as correct answers
        correct_indices = []
        for i, img in enumerate(grid):
            if img in agi_merch and len(correct_indices) < 4:
                correct_indices.append(i)
        
        # Ensure we have at least 2 correct answers
        if len(correct_indices) < 2:
            correct_indices = [0, 1, 2][:len(correct_indices) + 2]
        
        challenge = {
            "id": str(uuid.uuid4()),
            "grid": grid,
            "instructions": "Select all images with AGI House merch (AI-themed t-shirts, hoodies, and accessories)!",
            "targetProduct": "AGI House Merch",
            "correctCount": len(correct_indices),
            "correctIndices": correct_indices
        }
        
        response = {
            "success": True,
            "challenge": challenge
        }
        
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps(response).encode('utf-8'))
    
    def verify_captcha(self):
        """Verify CAPTCHA response"""
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        
        try:
            data = json.loads(post_data.decode('utf-8'))
            challenge_id = data.get('challengeId')
            selected_indices = data.get('selectedIndices', [])
            
            # For demo purposes, we'll simulate verification
            # In a real implementation, you'd validate against stored challenges
            
            if len(selected_indices) >= 2:
                # Simulate success
                success_token = str(uuid.uuid4())
                
                response = {
                    "success": True,
                    "token": success_token,
                    "message": "AGI Challenge Verified! Welcome to the future! 🤖✨",
                    "discountCode": "AGI10",
                    "discountMessage": "Unlock 10% off AGI House merch with code: AGI10",
                    "productSuggestion": "Check out our latest AI-themed collection!"
                }
            else:
                response = {
                    "success": False,
                    "error": "Incorrect selection. Try to identify AGI House merch!",
                    "attempts": 1,
                    "maxAttempts": 3,
                    "hint": "Look for AI-themed designs and AGI House branding"
                }
            
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps(response).encode('utf-8'))
            
        except json.JSONDecodeError:
            self.send_error(400, "Invalid JSON")
    
    def log_message(self, format, *args):
        """Custom log format"""
        print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] {format % args}")

def run_server(port=8000):
    """Run the AGI CAPTCHA server"""
    server_address = ('', port)
    httpd = HTTPServer(server_address, AGICaptchaHandler)
    
    print("🤖 AGI House Merch CAPTCHA Server Starting...")
    print("=" * 50)
    print(f"🚀 Server running at: http://localhost:{port}")
    print(f"📱 Health check: http://localhost:{port}/health")
    print(f"🎯 Demo page: http://localhost:{port}/")
    print("=" * 50)
    print("Press Ctrl+C to stop the server")
    print()
    
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n🛑 Server stopped by user")
        httpd.server_close()

if __name__ == '__main__':
    import sys
    
    port = 8000
    if len(sys.argv) > 1:
        try:
            port = int(sys.argv[1])
        except ValueError:
            print("❌ Invalid port number. Using default port 8000.")
    
    run_server(port)
