document.addEventListener('DOMContentLoaded', () => {
    const grid = document.getElementById('widgetGrid');
    const widgets = [
        `
        <html>
            <head>
                <style>
                    body {
                        margin: 0;
                        display: flex;
                        justify-content: center;
                        align-items: center;
                        height: 100%;
                        font-family: Arial, Helvetica, sans-serif;
                        background: #f0f0f0;
                        color: #333;
                    }
                    .date-container {
                        padding: 20px;
                        background: white;
                        border: 2px solid #ccc;
                        border-radius: 10px;
                        box-shadow: 2px 2px 5px rgba(0, 0, 0, 0.1);
                    }
                    .date-container h1 {
                        margin: 0;
                        font-size: 24px;
                    }
                </style>
            </head>
            <body>
                <div class="date-container">
                    <h1 id="currentDate"></h1>
                </div>
                <script>
                    const currentDate = new Date().toLocaleDateString(undefined, {
                        year: 'numeric',
                        month: 'long',
                        day: 'numeric',
                    });
                    document.getElementById('currentDate').textContent = "Today: " + currentDate;
                </script>
            </body>
        </html>
    `
    ]
    widgets.forEach(widget => {
        const iframe = document.createElement('iframe');
        iframe.className = 'widget';
        iframe.style.width = '100%';
        iframe.style.height = '200px';

        grid.appendChild(iframe);

        const doc = iframe.contentDocument || iframe.contentWindow.document;
        doc.open();
        doc.write(widget);
        doc.close();
    });
});