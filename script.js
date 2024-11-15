document.addEventListener('DOMContentLoaded', () => {
    const grid = document.getElementById('widgetGrid');
    const repo = 'boolYikes/widgets';
    const branch = 'main';
    const widgetDir = 'widgets';

    fetch(`https://api.github.com/repos/${repo}/contents/${widgetDir}?ref=${branch}`)
    .then(response => {
        if (!response.ok) {
            throw new Error(`Failed to fetch widget list: ${response.status}`);
        }
        return response.json();
    })
    .then(files => {
        files
        .filter(file => file.name.endsWith('.html'))
        .forEach(file => {
            const iframe = document.createElement('iframe');
            iframe.src = file.download_url;
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
        console.error(`Error loading widgets: ${error}`);
        grid.innerHTML = `<p>Error loading widgets. Try again later!</p>`;
    });

});