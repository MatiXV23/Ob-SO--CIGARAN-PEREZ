document.addEventListener('DOMContentLoaded', function () {
            
    const tooltipTitleCallback = (tooltipItems) => {
        const item = tooltipItems[0];
        let label = item.chart.data.labels[item.dataIndex];
        if (Array.isArray(label)) {
            return label.join(' ');
        }
        return label;
    };
    
    const wrapLabel = (label) => {
        const max_width = 16;
        if (label.length <= max_width) return label;
        const words = label.split(' ');
        let lines = [];
        let current_line = '';
        for (let word of words) {
            if ((current_line + word).length > max_width) {
                lines.push(current_line.trim());
                current_line = '';
            }
            current_line += word + ' ';
        }
        lines.push(current_line.trim());
        return lines.filter(line => line.length > 0);
    }

    const ctxRadar = document.getElementById('fileSystemRadarChart');
    if (ctxRadar) {
        new Chart(ctxRadar, {
            type: 'radar',
            data: {
                labels: ['Compatibilidad', 'Seguridad', 'Rendimiento', ['Tamaño Máximo', 'de Archivo'], 'Estabilidad', 'Recuperación'],
                datasets: [
                    {
                        label: 'NTFS (Windows)',
                        data: [3, 5, 4, 5, 5, 5],
                        backgroundColor: 'rgba(0, 115, 230, 0.2)',
                        borderColor: 'rgba(0, 115, 230, 1)',
                        borderWidth: 2,
                        pointBackgroundColor: 'rgba(0, 115, 230, 1)'
                    },
                    {
                        label: 'ext4 (Linux)',
                        data: [4, 4, 5, 5, 5, 5],
                        backgroundColor: 'rgba(82, 168, 255, 0.2)',
                        borderColor: 'rgba(82, 168, 255, 1)',
                        borderWidth: 2,
                        pointBackgroundColor: 'rgba(82, 168, 255, 1)'
                    },
                        {
                        label: 'FAT32',
                        data: [5, 1, 3, 1, 4, 1],
                        backgroundColor: 'rgba(184, 219, 255, 0.4)',
                        borderColor: 'rgba(184, 219, 255, 1)',
                        borderWidth: 2,
                        pointBackgroundColor: 'rgba(184, 219, 255, 1)'
                    }
                ]
            },
            options: {
                maintainAspectRatio: false,
                plugins: {
                    tooltip: {
                        callbacks: {
                            title: tooltipTitleCallback
                        }
                    },
                    legend: {
                        position: 'bottom',
                    }
                },
                scales: {
                    r: {
                        beginAtZero: true,
                        max: 5,
                        pointLabels: {
                            font: {
                                size: 12
                            }
                        },
                        ticks: {
                            stepSize: 1,
                            backdropColor: 'rgba(255, 255, 255, 0.75)'
                        }
                    }
                }
            }
        });
    }
});