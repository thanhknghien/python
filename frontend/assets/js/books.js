document.addEventListener('DOMContentLoaded', async () => {
    try {
        const books = await fetchAPI('books/');
        renderBooks(books, 'book-list');
    } catch (error) {
        console.error('Error fetching books:', error);
    }
});

function renderBooks(books, containerId) {
    const container = document.getElementById(containerId);
    container.innerHTML = books.map(book => `
        <div class="book">
            <img src="${book.ImagePath || '../assets/images/placeholder.jpg'}" alt="${book.Title}">
            <h3>${book.Title}</h3>
            <p>Author: ${book.Author || 'Unknown'}</p>
            <p>Price: $${book.Price}</p>
            <p>Stock: ${book.StockQuantity}</p>
            <p>Category: ${book.CategoryID ? book.CategoryID.Name : 'None'}</p>
        </div>
    `).join('');
}

async function filterBooks() {
    const categoryId = document.getElementById('category-id').value;
    if (!categoryId) {
        alert('Please enter a Category ID');
        return;
    }
    try {
        const books = await fetchAPI(`books/by-category/${categoryId}/`);
        renderBooks(books, 'filtered-books');
    } catch (error) {
        console.error('Error filtering books:', error);
        document.getElementById('filtered-books').innerHTML = '<p>No books found</p>';
    }
}