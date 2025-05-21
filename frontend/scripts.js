document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('subscription-form');
    const emailInput = document.getElementById('email');
    const quotesContainer = document.getElementById('quotes-container');

    form.addEventListener('submit', function(event) {
        event.preventDefault();
        const email = emailInput.value;
        subscribe(email);
    });

    function subscribe(email) {
        fetch('http://localhost:5000/subscribe', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ email: email })
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                alert('Subscription successful!');
                emailInput.value = '';
            } else {
                alert('Subscription failed. Please try again.');
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('An error occurred. Please try again.');
        });
    }

    function fetchRecentQuotes() {
        fetch('http://localhost:5000/recent-quotes')
        .then(response => response.json())
        .then(data => {
            displayQuotes(data.quotes);
        })
        .catch(error => {
            console.error('Error:', error);
        });
    }

    function displayQuotes(quotes) {
        quotesContainer.innerHTML = '';
        quotes.forEach(quote => {
            const quoteElement = document.createElement('div');
            quoteElement.classList.add('quote');
            quoteElement.textContent = `"${quote.text}" - ${quote.author}`;
            quotesContainer.appendChild(quoteElement);
        });
    }

    fetchRecentQuotes();
});
