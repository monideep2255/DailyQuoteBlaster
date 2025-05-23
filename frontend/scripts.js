document.addEventListener('DOMContentLoaded', function() {
    // Form elements
    const form = document.getElementById('subscription-form');
    const emailInput = document.getElementById('email');
    const phoneInput = document.getElementById('phone');
    const morningCheckbox = document.getElementById('morning');
    const eveningCheckbox = document.getElementById('evening');
    const categoriesSelect = document.getElementById('categories');
    
    // Quotes container
    const quotesContainer = document.getElementById('quotes-container');
    
    // Toast elements
    const toast = document.getElementById('toast');
    const toastMessage = document.getElementById('toast-message');
    const toastClose = document.getElementById('toast-close');

    // Event listeners
    form.addEventListener('submit', function(event) {
        event.preventDefault();
        
        // Get form values
        const email = emailInput.value;
        const phone = phoneInput.value;
        const morning = morningCheckbox.checked;
        const evening = eveningCheckbox.checked;
        
        // Get selected categories
        const selectedCategories = Array.from(categoriesSelect.selectedOptions).map(option => option.value);
        
        // Validate at least one delivery time is selected
        if (!morning && !evening) {
            showToast('Please select at least one delivery time (morning or evening)', 'error');
            return;
        }
        
        // Validate at least one contact method
        if (!email && !phone) {
            showToast('Please provide either an email or phone number', 'error');
            return;
        }
        
        // Submit subscription
        subscribe({
            email,
            phone,
            deliveryTimes: {
                morning,
                evening
            },
            categories: selectedCategories
        });
    });
    
    // Close toast
    toastClose.addEventListener('click', function() {
        toast.classList.remove('show');
    });

    // Subscribe function
    function subscribe(userData) {
        fetch('/api/subscribe', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(userData)
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                // Clear form
                form.reset();
                
                // Show success message
                showToast('Subscription successful! You will receive your first quote soon.', 'success');
            } else {
                showToast(data.message || 'Subscription failed. Please try again.', 'error');
            }
        })
        .catch(error => {
            console.error('Error:', error);
            showToast('An error occurred. Please try again later.', 'error');
        });
    }

    // Show toast message
    function showToast(message, type = 'success') {
        toastMessage.textContent = message;
        
        // Set toast color based on type
        if (type === 'error') {
            toast.style.backgroundColor = '#f72585';
        } else {
            toast.style.backgroundColor = '#4cc9f0';
        }
        
        // Show toast
        toast.classList.add('show');
        
        // Auto-hide after 5 seconds
        setTimeout(() => {
            toast.classList.remove('show');
        }, 5000);
    }

    // Category filter elements
    const categoryFilter = document.getElementById('category-filter');
    const refreshQuotesBtn = document.getElementById('refresh-quotes');
    const emptyQuotesEl = document.getElementById('empty-quotes');
    
    // Store all quotes for filtering
    let allQuotes = [];
    
    // Fetch recent quotes
    function fetchRecentQuotes() {
        fetch('/api/quotes/recent')
        .then(response => response.json())
        .then(data => {
            allQuotes = data; // Store all quotes
            filterAndDisplayQuotes();
        })
        .catch(error => {
            console.error('Error fetching quotes:', error);
            
            // If API fails, show sample quotes
            allQuotes = [
                {
                    text: "The best way to predict the future is to create it.",
                    author: "Abraham Lincoln",
                    date: "2025-05-23",
                    category: "motivational"
                },
                {
                    text: "Whatever anybody says or does, assume positive intent.",
                    author: "Indra Nooyi",
                    date: "2025-05-22",
                    category: "wisdom"
                },
                {
                    text: "Choose your suffering before suffering chooses you!",
                    author: "Monideep",
                    date: "2025-05-21",
                    category: "growth"
                },
                {
                    text: "The right decision is always harder in the short term but better in the long term.",
                    author: "Dave Ramsey", 
                    date: "2025-05-20",
                    category: "decisions"
                },
                {
                    text: "If you will live like no one else, later you can live like no one else.",
                    author: "Dave Ramsey",
                    date: "2025-05-19",
                    category: "success"
                }
            ];
            filterAndDisplayQuotes();
        });
    }
    
    // Filter quotes by category and display
    function filterAndDisplayQuotes() {
        const selectedCategory = categoryFilter.value;
        
        // Filter quotes by category (if not 'all')
        const filteredQuotes = selectedCategory === 'all' 
            ? allQuotes 
            : allQuotes.filter(quote => quote.category === selectedCategory);
            
        // Display quotes or empty state
        if (filteredQuotes.length > 0) {
            displayQuotes(filteredQuotes);
            quotesContainer.style.display = 'grid';
            emptyQuotesEl.style.display = 'none';
        } else {
            quotesContainer.style.display = 'none';
            emptyQuotesEl.style.display = 'block';
        }
    }

    // Display quotes in a modern card layout
    function displayQuotes(quotes) {
        quotesContainer.innerHTML = '';
        
        quotes.forEach(quote => {
            // Create quote card
            const quoteCard = document.createElement('div');
            quoteCard.classList.add('quote-card');
            
            // Add category badge
            const categoryBadge = document.createElement('span');
            categoryBadge.classList.add('quote-category', quote.category);
            categoryBadge.textContent = quote.category;
            quoteCard.appendChild(categoryBadge);
            
            // Add quote text
            const quoteText = document.createElement('div');
            quoteText.classList.add('quote-text');
            quoteText.textContent = `"${quote.text}"`;
            quoteCard.appendChild(quoteText);
            
            // Add author
            const quoteAuthor = document.createElement('div');
            quoteAuthor.classList.add('quote-author');
            quoteAuthor.textContent = quote.author;
            quoteCard.appendChild(quoteAuthor);
            
            // Add date
            if (quote.date) {
                const quoteDate = document.createElement('div');
                quoteDate.classList.add('quote-date');
                quoteDate.textContent = formatDate(quote.date);
                quoteCard.appendChild(quoteDate);
            }
            
            // Add to container
            quotesContainer.appendChild(quoteCard);
        });
    }
    
    // Event listeners for filtering
    categoryFilter.addEventListener('change', filterAndDisplayQuotes);
    
    // Additional sample quotes for refresh functionality
    const additionalQuotes = [
        {
            text: "Don't watch the clock; do what it does. Keep going.",
            author: "Sam Levenson",
            date: "2025-05-22",
            category: "motivational"
        },
        {
            text: "The only limit to our realization of tomorrow is our doubts of today.",
            author: "Franklin D. Roosevelt",
            date: "2025-05-21",
            category: "growth"
        },
        {
            text: "The journey of a thousand miles begins with one step.",
            author: "Lao Tzu",
            date: "2025-05-20",
            category: "wisdom"
        },
        {
            text: "It's not about having time, it's about making time.",
            author: "Unknown",
            date: "2025-05-19", 
            category: "decisions"
        },
        {
            text: "Success is not final, failure is not fatal: It is the courage to continue that counts.",
            author: "Winston Churchill",
            date: "2025-05-18",
            category: "success"
        },
        {
            text: "Your time is limited, don't waste it living someone else's life.",
            author: "Steve Jobs",
            date: "2025-05-17",
            category: "wisdom"
        },
        {
            text: "You are never too old to set another goal or to dream a new dream.",
            author: "C.S. Lewis",
            date: "2025-05-16",
            category: "growth"
        },
        {
            text: "The best time to plant a tree was 20 years ago. The second best time is now.",
            author: "Chinese Proverb",
            date: "2025-05-15",
            category: "motivational"
        }
    ];
    
    // Counter to track which quote set to display
    let quoteSetIndex = 0;
    
    // Refresh quotes when button is clicked
    refreshQuotesBtn.addEventListener('click', function() {
        const btn = this;
        btn.disabled = true;
        btn.innerHTML = '<i class="fas fa-sync-alt fa-spin"></i> Loading...';
        
        // Rotate between different sets of quotes
        quoteSetIndex = (quoteSetIndex + 1) % 3;
        
        // Show different quotes based on counter
        if (quoteSetIndex === 1) {
            allQuotes = additionalQuotes;
        } else if (quoteSetIndex === 2) {
            allQuotes = [
                {
                    text: "Believe you can and you're halfway there.",
                    author: "Theodore Roosevelt",
                    date: "2025-05-23",
                    category: "motivational"
                },
                {
                    text: "Life is 10% what happens to you and 90% how you react to it.",
                    author: "Charles R. Swindoll",
                    date: "2025-05-22",
                    category: "wisdom"
                },
                {
                    text: "What you do today can improve all your tomorrows.",
                    author: "Ralph Marston",
                    date: "2025-05-21",
                    category: "growth"
                },
                {
                    text: "It always seems impossible until it's done.",
                    author: "Nelson Mandela", 
                    date: "2025-05-20",
                    category: "decisions"
                },
                {
                    text: "Don't let yesterday take up too much of today.",
                    author: "Will Rogers",
                    date: "2025-05-19",
                    category: "success"
                }
            ];
        } else {
            allQuotes = [
                {
                    text: "The best way to predict the future is to create it.",
                    author: "Abraham Lincoln",
                    date: "2025-05-23",
                    category: "motivational"
                },
                {
                    text: "Whatever anybody says or does, assume positive intent.",
                    author: "Indra Nooyi",
                    date: "2025-05-22",
                    category: "wisdom"
                },
                {
                    text: "Choose your suffering before suffering chooses you!",
                    author: "Monideep",
                    date: "2025-05-21",
                    category: "growth"
                },
                {
                    text: "The right decision is always harder in the short term but better in the long term.",
                    author: "Dave Ramsey", 
                    date: "2025-05-20",
                    category: "decisions"
                },
                {
                    text: "If you will live like no one else, later you can live like no one else.",
                    author: "Dave Ramsey",
                    date: "2025-05-19",
                    category: "success"
                }
            ];
        }
        
        // Show the new quotes
        filterAndDisplayQuotes();
        
        // Reset button after a short delay
        setTimeout(() => {
            btn.disabled = false;
            btn.innerHTML = '<i class="fas fa-sync-alt"></i> Refresh Quotes';
        }, 300);
    });
    
    // Format date as "Month Day, Year"
    function formatDate(dateString) {
        const date = new Date(dateString);
        return date.toLocaleDateString('en-US', { 
            month: 'long', 
            day: 'numeric', 
            year: 'numeric' 
        });
    }

    // Initialize
    fetchRecentQuotes();
    
    // Add text-center class
    document.querySelectorAll('.text-center').forEach(el => {
        el.style.textAlign = 'center';
    });
});
