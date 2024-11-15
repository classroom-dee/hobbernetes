document.addEventListener('DOMContentLoaded', () => {
    const grid = document.getElementById('widgetGrid');
    const baseURL = 'https://boolYikes.github.io/widgets/'; // Your GitHub Pages URL for the widgets directory

    // Fetch the widget list from widgets.json
    fetch(`${baseURL}widgets.json`)
    .then(response => {
        if (!response.ok) {
            throw new Error('Failed to fetch widget list');
        }
        return response.json();
    })
    .then(widgets => {
    // For each widget in the list, create an iframe
        widgets.forEach(widget => {
        const iframe = document.createElement('iframe');
        iframe.src = `${baseURL}${widget}`; // Embed widget from GitHub Pages
        iframe.className = 'widget';
        iframe.style.width = '100%';
        iframe.style.height = '200px';
        
        const container = document.createElement('div');
        container.className = 'widget';
        container.appendChild(iframe);

        grid.appendChild(container);
        });
    })
    .catch(error => {
        console.error('Error loading widgets:', error);
        grid.innerHTML = `<p>Error loading widgets.</p>`;
    });
});