/**
 * AI Business Growth Platform - Dashboard JavaScript
 * Handles all API calls and frontend interactions
 */

// ==================== API BASE URL ====================
const API_BASE = '/api';

// ==================== UTILITY FUNCTIONS ====================

/**
 * Show loading state
 */
function showLoading(element) {
    element.innerHTML = '<div class="loading"><i class="fas fa-spinner fa-spin"></i> Processing...</div>';
}

/**
 * Display error message
 */
function showError(element, message) {
    element.innerHTML = `<div class="error-message"><i class="fas fa-exclamation-circle"></i> ${message}</div>`;
    element.style.display = 'block';
}

/**
 * Display success result
 */
function showResult(element, data) {
    element.innerHTML = `<div class="success-message"><pre>${JSON.stringify(data, null, 2)}</pre></div>`;
    element.style.display = 'block';
}

/**
 * Fetch API wrapper
 */
async function fetchAPI(endpoint, data) {
    try {
        const response = await fetch(endpoint, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data)
        });
        
        if (!response.ok) {
            throw new Error(`HTTP ${response.status}: ${response.statusText}`);
        }
        
        return await response.json();
    } catch (error) {
        console.error('API Error:', error);
        throw error;
    }
}

// ==================== MODULE 1: MARKET INTELLIGENCE ====================

/**
 * Handle Sentiment Analysis submission
 */
async function handleSentimentSubmit(event) {
    event.preventDefault();
    const input = document.getElementById('sentiment-input').value;
    const resultDiv = document.getElementById('sentiment-result');
    
    showLoading(resultDiv);
    
    try {
        const result = await fetchAPI(`${API_BASE}/market/sentiment`, {
            feedback: input
        });
        
        // Format result nicely
        const formatted = {
            'Sentiment': result.sentiment?.toUpperCase() || 'N/A',
            'Confidence': `${(result.confidence * 100).toFixed(1)}%`,
            'Summary': result.summary || 'No summary available'
        };
        
        showResult(resultDiv, formatted);
    } catch (error) {
        showError(resultDiv, `Sentiment Analysis failed: ${error.message}`);
    }
}

/**
 * Handle Competitor Benchmark submission
 */
async function handleBenchmarkSubmit(event) {
    event.preventDefault();
    const input = document.getElementById('benchmark-input').value;
    const resultDiv = document.getElementById('benchmark-result');
    
    showLoading(resultDiv);
    
    try {
        const result = await fetchAPI(`${API_BASE}/market/benchmark`, {
            brand: input
        });
        
        const formatted = {
            'Market Score': `${result.market_score}/100`,
            'Trend': result.trend?.toUpperCase() || 'N/A',
            'Position': result.market_position || 'N/A',
            'Key Strength': result.key_strength || 'N/A',
            'Key Weakness': result.key_weakness || 'N/A'
        };
        
        showResult(resultDiv, formatted);
    } catch (error) {
        showError(resultDiv, `Benchmark failed: ${error.message}`);
    }
}

// ==================== MODULE 2: SMART PRICING ENGINE ====================

/**
 * Handle Dynamic Pricing submission
 */
async function handlePricingSubmit(event) {
    event.preventDefault();
    const cost = document.getElementById('cost-input').value;
    const demand = document.getElementById('demand-input').value;
    const competitor = document.getElementById('competitor-input').value;
    const resultDiv = document.getElementById('pricing-result');
    
    showLoading(resultDiv);
    
    try {
        const result = await fetchAPI(`${API_BASE}/pricing/optimize`, {
            cost: parseFloat(cost),
            demand_index: parseFloat(demand),
            competitor_price: parseFloat(competitor)
        });
        
        if (result.error) {
            showError(resultDiv, result.error);
            return;
        }
        
        const formatted = {
            'Optimal Price': `$${result.optimal_price || 0}`,
            'Margin': `${result.margin_percent || 0}%`,
            'Recommendation': result.pricing_reason || 'N/A',
            'Competitor Analysis': result.competitor_analysis || 'N/A'
        };
        
        showResult(resultDiv, formatted);
    } catch (error) {
        showError(resultDiv, `Pricing optimization failed: ${error.message}`);
    }
}

// ==================== MODULE 3: COMPLIANCE & RISK MONITORING ====================

/**
 * Handle Compliance Check submission
 */
async function handleComplianceSubmit(event) {
    event.preventDefault();
    const input = document.getElementById('compliance-input').value;
    const resultDiv = document.getElementById('compliance-result');
    
    showLoading(resultDiv);
    
    try {
        const result = await fetchAPI(`${API_BASE}/compliance/check`, {
            marketing_text: input
        });
        
        const riskColor = result.risk_level === 'high' ? '🔴' : 
                         result.risk_level === 'medium' ? '🟡' : '🟢';
        
        const formatted = {
            'Risk Level': `${riskColor} ${result.risk_level?.toUpperCase() || 'UNKNOWN'}`,
            'GDPR Compliant': result.gdpr_compliant ? '✓ Yes' : '✗ No',
            'Flagged Phrases': result.flagged_phrases?.length > 0 ? result.flagged_phrases.join(', ') : 'None',
            'Suggestions': result.suggestions?.length > 0 ? result.suggestions.join('; ') : 'Your text looks compliant!'
        };
        
        showResult(resultDiv, formatted);
    } catch (error) {
        showError(resultDiv, `Compliance check failed: ${error.message}`);
    }
}

// ==================== MODULE 4: AI CHATBOT ====================

let chatMessages = [];

/**
 * Add message to chat display
 */
function addChatMessage(message, sender) {
    const chatHistory = document.getElementById('chat-history');
    const messageDiv = document.createElement('div');
    messageDiv.className = `chat-message ${sender}`;
    messageDiv.innerHTML = `<span class="message-text">${escapeHtml(message)}</span>`;
    chatHistory.appendChild(messageDiv);
    chatHistory.scrollTop = chatHistory.scrollHeight;
}

/**
 * Escape HTML to prevent XSS
 */
function escapeHtml(text) {
    const map = {
        '&': '&amp;',
        '<': '&lt;',
        '>': '&gt;',
        '"': '&quot;',
        "'": '&#039;'
    };
    return text.replace(/[&<>"']/g, m => map[m]);
}

/**
 * Handle Chat submission
 */
async function handleChatSubmit(event) {
    event.preventDefault();
    const input = document.getElementById('chat-input');
    const message = input.value;
    
    if (!message.trim()) return;
    
    // Add user message
    addChatMessage(message, 'user');
    input.value = '';
    chatMessages.push({ role: 'user', content: message });
    
    try {
        const result = await fetchAPI(`${API_BASE}/chat`, {
            message: message,
            history: chatMessages.slice(0, -1)  // Exclude current message for history
        });
        
        if (result.status === 'error') {
            addChatMessage(`Error: ${result.response}`, 'bot');
        } else {
            const response = result.response || 'I did not understand that. Please try again.';
            addChatMessage(response, 'bot');
            chatMessages.push({ role: 'assistant', content: response });
        }
    } catch (error) {
        addChatMessage(`Connection error: ${error.message}`, 'bot');
    }
}

// ==================== MODULE 5: PREDICTIVE ANALYTICS ====================

/**
 * Handle Predictive Analytics submission
 */
async function handlePredictionSubmit(event) {
    event.preventDefault();
    const input = document.getElementById('prediction-input').value;
    const resultDiv = document.getElementById('prediction-result');
    
    showLoading(resultDiv);
    
    try {
        const result = await fetchAPI(`${API_BASE}/predict/customer`, {
            history_data: input
        });
        
        const riskColor = result.churn_risk === 'high' ? '🔴' :
                         result.churn_risk === 'medium' ? '🟡' : '🟢';
        
        const formatted = {
            'Churn Risk': `${riskColor} ${result.churn_risk?.toUpperCase() || 'UNKNOWN'}`,
            'Churn Probability': `${result.churn_probability || 0}%`,
            'Next Best Action': result.next_best_action || 'N/A',
            'Campaign Timing': result.campaign_timing || 'N/A',
            'Recommended Channel': result.recommended_channel || 'N/A'
        };
        
        showResult(resultDiv, formatted);
    } catch (error) {
        showError(resultDiv, `Prediction failed: ${error.message}`);
    }
}

// ==================== MODULE 6: PERSONALIZATION ENGINE ====================

/**
 * Handle Personalization submission
 */
async function handlePersonalizationSubmit(event) {
    event.preventDefault();
    const input = document.getElementById('personalization-input').value;
    const resultDiv = document.getElementById('personalization-result');
    
    showLoading(resultDiv);
    
    try {
        const result = await fetchAPI(`${API_BASE}/personalize`, {
            user_profile: input
        });
        
        let formatted = {};
        if (result.recommended_products) {
            result.recommended_products.forEach((product, index) => {
                formatted[`Product ${index + 1}`] = `${product.name} (${product.priority?.toUpperCase() || 'NORMAL'})`;
                formatted[`  Reason`] = product.reason || 'N/A';
            });
        }
        
        showResult(resultDiv, formatted);
    } catch (error) {
        showError(resultDiv, `Personalization failed: ${error.message}`);
    }
}

// ==================== SIDEBAR NAVIGATION ====================

/**
 * Initialize sidebar navigation
 */
document.addEventListener('DOMContentLoaded', function() {
    const sidebarLinks = document.querySelectorAll('.sidebar-link');
    
    sidebarLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            
            // Remove active from all links
            sidebarLinks.forEach(l => l.classList.remove('active'));
            
            // Add active to clicked link
            this.classList.add('active');
            
            // Scroll to section
            const sectionId = this.getAttribute('href').slice(1);
            const section = document.getElementById(sectionId);
            if (section) {
                section.scrollIntoView({ behavior: 'smooth' });
            }
        });
    });
});

// ==================== REAL-TIME UPDATES ====================

/**
 * Check system health periodically
 */
function checkSystemHealth() {
    fetch('/api/health')
        .then(response => response.json())
        .then(data => {
            console.log('System Status:', data);
        })
        .catch(error => console.error('Health check failed:', error));
}

// Check health every 30 seconds
setInterval(checkSystemHealth, 30000);

console.log('✓ Dashboard.js loaded successfully');
