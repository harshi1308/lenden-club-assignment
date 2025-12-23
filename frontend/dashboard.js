const API_URL = 'http://localhost:5000';
let currentSortKey = 'timestamp';
let sortDirection = 'desc';
let allTransactions = [];

// Check authentication
if (!localStorage.getItem('token')) {
    window.location.href = 'index.html';
}

const token = localStorage.getItem('token');
const userId = localStorage.getItem('user_id');
const username = localStorage.getItem('username');

document.getElementById('username').textContent = `Welcome, ${username}!`;

async function loadBalance() {
    try {
        const response = await fetch(`${API_URL}/balance`, {
            headers: {
                'Authorization': `Bearer ${token}`
            }
        });

        if (response.ok) {
            const data = await response.json();
            document.getElementById('balance').textContent = data.balance.toFixed(2);
        } else if (response.status === 401) {
            logout();
        }
    } catch (error) {
        console.error('Error loading balance:', error);
    }
}

async function loadUsers() {
    try {
        const response = await fetch(`${API_URL}/users`, {
            headers: {
                'Authorization': `Bearer ${token}`
            }
        });

        if (response.ok) {
            const data = await response.json();
            const select = document.getElementById('receiver-username');
            select.innerHTML = '<option value="">Select Receiver</option>';
            
            data.users.forEach(user => {
                const option = document.createElement('option');
                option.value = user.username;
                option.textContent = user.username;
                select.appendChild(option);
            });
        }
    } catch (error) {
        console.error('Error loading users:', error);
    }
}

async function transfer() {
    const receiver_username = document.getElementById('receiver-username').value;
    const amount = document.getElementById('amount').value;
    const messageDiv = document.getElementById('transfer-message');

    if (!receiver_username || !amount) {
        showMessage('Please fill in all fields', 'error');
        return;
    }

    try {
        const response = await fetch(`${API_URL}/transfer`, {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${token}`,
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ receiver_username, amount: parseFloat(amount) })
        });

        const data = await response.json();

        if (response.ok) {
            showMessage(`Transfer successful! New balance: $${data.new_balance.toFixed(2)}`, 'success');
            document.getElementById('receiver-username').value = '';
            document.getElementById('amount').value = '';
            
            // Update balance and reload transactions
            loadBalance();
            loadTransactions();
        } else {
            showMessage(`Error: ${data.error}`, 'error');
        }
    } catch (error) {
        showMessage('Network error. Please try again.', 'error');
        console.error('Error:', error);
    }
}

async function loadTransactions() {
    try {
        const response = await fetch(`${API_URL}/transactions/${userId}`, {
            headers: {
                'Authorization': `Bearer ${token}`
            }
        });

        if (response.ok) {
            const data = await response.json();
            allTransactions = data.transactions;
            displayTransactions();
        }
    } catch (error) {
        console.error('Error loading transactions:', error);
    }
}

function displayTransactions() {
    const tbody = document.getElementById('transactions-body');
    
    if (allTransactions.length === 0) {
        tbody.innerHTML = '<tr><td colspan="5" class="no-data">No transactions yet</td></tr>';
        return;
    }

    // Sort transactions
    const sorted = [...allTransactions].sort((a, b) => {
        let valA = a[currentSortKey];
        let valB = b[currentSortKey];

        if (currentSortKey === 'amount') {
            valA = parseFloat(valA);
            valB = parseFloat(valB);
        }

        if (sortDirection === 'asc') {
            return valA > valB ? 1 : -1;
        } else {
            return valA < valB ? 1 : -1;
        }
    });

    tbody.innerHTML = sorted.map(txn => {
        const date = new Date(txn.timestamp).toLocaleString();
        const typeClass = txn.type === 'SENT' ? 'type-sent' : 'type-received';
        const statusClass = txn.status === 'SUCCESS' ? 'status-success' : 'status-failed';
        const amountSign = txn.type === 'SENT' ? '-' : '+';
        
        return `
            <tr>
                <td>${date}</td>
                <td class="${typeClass}">${txn.type}</td>
                <td>${txn.other_party}</td>
                <td>${amountSign}$${txn.amount.toFixed(2)}</td>
                <td class="${statusClass}">${txn.status}</td>
            </tr>
        `;
    }).join('');
}

function sortTransactions(key) {
    if (currentSortKey === key) {
        sortDirection = sortDirection === 'asc' ? 'desc' : 'asc';
    } else {
        currentSortKey = key;
        sortDirection = 'desc';
    }
    displayTransactions();
}

function showMessage(message, type) {
    const messageDiv = document.getElementById('transfer-message');
    messageDiv.textContent = message;
    messageDiv.className = `message ${type}`;
    
    setTimeout(() => {
        messageDiv.textContent = '';
        messageDiv.className = 'message';
    }, 5000);
}

function logout() {
    localStorage.clear();
    window.location.href = 'index.html';
}

// Load initial data
loadBalance();
loadUsers();
loadTransactions();

// Refresh data every 10 seconds
setInterval(() => {
    loadBalance();
    loadTransactions();
}, 10000);
