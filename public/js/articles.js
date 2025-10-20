/**
 * Articles Interface Controller
 */

const articlesState = {
    allResults: [],
    currentPage: 0,
    resultsPerPage: 9,
    isLoading: false
};

document.addEventListener('DOMContentLoaded', function() {
    const articlesInput = document.getElementById('articlesInput');
    const articleSearchBtn = document.getElementById('articleSearchBtn');

    articlesInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
            e.preventDefault();
            searchArticles();
        }
    });

    articleSearchBtn.addEventListener('click', searchArticles);
});

async function searchArticles() {
    const query = document.getElementById('articlesInput').value.trim();
    if (!query || articlesState.isLoading) return;

    articlesState.isLoading = true;
    document.getElementById('articleSearchBtn').disabled = true;

    try {
        const response = await api.search(query, 'clockify', 20);
        articlesState.allResults = response.results || [];
        articlesState.currentPage = 0;

        if (articlesState.allResults.length === 0) {
            document.getElementById('articlesResults').innerHTML = '<p class="empty-state">No articles found. Try different keywords.</p>';
            document.getElementById('pagination').style.display = 'none';
        } else {
            displayArticlesPage();
        }
    } catch (error) {
        document.getElementById('articlesResults').innerHTML = `<p class="error-message">Error: ${error.message}</p>`;
    } finally {
        articlesState.isLoading = false;
        document.getElementById('articleSearchBtn').disabled = false;
    }
}

function displayArticlesPage() {
    const { allResults, currentPage, resultsPerPage } = articlesState;
    const start = currentPage * resultsPerPage;
    const end = start + resultsPerPage;
    const pageResults = allResults.slice(start, end);

    const filterHighConf = document.getElementById('filterHighConf').checked;
    const filtered = filterHighConf ? pageResults.filter(r => (r.confidence || 0) > 50) : pageResults;

    const html = filtered.map(article => createArticleCard(article)).join('');
    document.getElementById('articlesResults').innerHTML = html || '<p class="empty-state">No results match your filters.</p>';

    // Update pagination
    const totalPages = Math.ceil(allResults.length / resultsPerPage);
    if (totalPages > 1) {
        document.getElementById('pagination').style.display = 'flex';
        document.getElementById('pageInfo').textContent = `Page ${currentPage + 1} of ${totalPages}`;
        document.getElementById('prevBtn').disabled = currentPage === 0;
        document.getElementById('nextBtn').disabled = currentPage === totalPages - 1;

        document.getElementById('prevBtn').onclick = () => {
            articlesState.currentPage--;
            displayArticlesPage();
        };
        document.getElementById('nextBtn').onclick = () => {
            articlesState.currentPage++;
            displayArticlesPage();
        };
    } else {
        document.getElementById('pagination').style.display = 'none';
    }
}

function createArticleCard(article) {
    const confidence = article.confidence || 0;
    const level = confidence > 75 ? 'high' : confidence > 50 ? 'medium' : 'low';
    const emoji = confidence > 75 ? '🟢' : confidence > 50 ? '🟡' : '🔴';

    return `
        <div class="article-card" onclick="openArticle('${encodeURIComponent(JSON.stringify(article))}')">
            <h3>${article.title || 'Untitled'}</h3>
            <p>${(article.content || 'No content').substring(0, 150)}...</p>
            <div class="article-meta">
                <span class="confidence-badge confidence-${level}">${emoji} ${confidence.toFixed(0)}%</span>
                <span style="font-size: 0.75rem;">${article.namespace || 'unknown'}</span>
            </div>
        </div>
    `;
}

function openArticle(encodedData) {
    try {
        const article = JSON.parse(decodeURIComponent(encodedData));
        const url = article.url;
        if (url) {
            window.open(url, '_blank');
        }
    } catch (e) {
        console.error('Failed to open article:', e);
    }
}

// Filter change listener
document.addEventListener('DOMContentLoaded', function() {
    const filterCheckbox = document.getElementById('filterHighConf');
    if (filterCheckbox) {
        filterCheckbox.addEventListener('change', () => {
            if (articlesState.allResults.length > 0) {
                displayArticlesPage();
            }
        });
    }
});
