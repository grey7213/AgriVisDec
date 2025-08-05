// AgriDec 主JavaScript文件
$(document).ready(function() {
    console.log('AgriDec 系统已加载');
    
    // 初始化通知容器
    if ($('#notification-container').length === 0) {
        $('body').prepend('<div id="notification-container" class="position-fixed" style="top: 20px; right: 20px; z-index: 9999;"></div>');
    }
    
    // 初始化数据采集按钮
    $('.btn-collect-data').click(function() {
        const $btn = $(this);
        const website = $btn.data('website');
        const dataType = $btn.data('type') || getDataTypeFromWebsite(website);
        const originalText = $btn.text();
        const originalHtml = $btn.html();
        
        // 显示加载状态
        $btn.prop('disabled', true)
            .html('<span class="loading-spinner"></span> 采集中...');
        
        // 发送采集请求
        $.ajax({
            url: '/api/crawl-data',
            method: 'POST',
            contentType: 'application/json',
            data: JSON.stringify({
                website: website,
                data_type: dataType,
                region: '全国',
                max_pages: 2
            }),
            timeout: 120000, // 2分钟超时
            success: function(response) {
                if (response.success) {
                    showNotification(`${getWebsiteName(website)}数据采集成功！获取 ${response.count || 0} 条记录`, 'success');
                    // 刷新相关数据显示
                    refreshDataDisplay(dataType);
                } else {
                    showNotification(`数据采集失败：${response.error || '未知错误'}`, 'error');
                }
            },
            error: function(xhr, status, error) {
                let errorMsg = '请求失败';
                if (status === 'timeout') {
                    errorMsg = '请求超时，数据采集可能仍在后台进行';
                } else if (xhr.status === 500) {
                    errorMsg = '服务器内部错误，请稍后重试';
                } else if (xhr.status === 0) {
                    errorMsg = '网络连接失败，请检查网络';
                } else {
                    errorMsg = `请求失败 (${xhr.status}): ${error}`;
                }
                showNotification(errorMsg, 'error');
            },
            complete: function() {
                $btn.prop('disabled', false).html(originalHtml);
            }
        });
    });
    
    // 初始化图表刷新按钮
    $('.btn-refresh-chart').click(function() {
        const chartType = $(this).data('chart-type');
        refreshChart(chartType);
    });
    
    // 初始化数据表格
    initializeDataTables();
    
    // 定时刷新系统状态（每5分钟）
    setInterval(function() {
        updateSystemStatus();
    }, 5 * 60 * 1000);
    
    // 初始化系统状态
    updateSystemStatus();
    
    // 初始化工具提示
    if (typeof bootstrap !== 'undefined') {
        var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
        var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
            return new bootstrap.Tooltip(tooltipTriggerEl);
        });
    }
    
    // 自动隐藏警告消息
    setTimeout(function() {
        $('.alert').fadeOut();
    }, 5000);
});

// 显示通知消息
function showNotification(message, type = 'info', duration = 5000) {
    const alertClass = type === 'success' ? 'alert-success' : 
                      type === 'error' ? 'alert-danger' : 
                      type === 'warning' ? 'alert-warning' : 'alert-info';
    
    const iconClass = type === 'success' ? 'fas fa-check-circle' :
                     type === 'error' ? 'fas fa-exclamation-circle' :
                     type === 'warning' ? 'fas fa-exclamation-triangle' : 'fas fa-info-circle';
    
    const notification = $(`
        <div class="alert ${alertClass} alert-dismissible fade show" role="alert" style="min-width: 300px;">
            <i class="${iconClass} me-2"></i>${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        </div>
    `);
    
    $('#notification-container').append(notification);
    
    // 自动消失
    setTimeout(function() {
        notification.alert('close');
    }, duration);
}

// 刷新数据显示
function refreshDataDisplay(dataType) {
    switch(dataType) {
        case 'seed_prices':
            if (typeof refreshSeedData === 'function') {
                refreshSeedData();
            }
            break;
        case 'weather':
            if (typeof refreshWeatherData === 'function') {
                refreshWeatherData();
            }
            break;
        case 'farm_machines':
            if (typeof refreshMachineData === 'function') {
                refreshMachineData();
            }
            break;
    }
    
    // 刷新统计数据
    updateDataStatistics();
}

// 刷新图表
function refreshChart(chartType) {
    console.log('刷新图表:', chartType);
    
    const $chartContainer = $(`#${chartType}-chart`);
    if ($chartContainer.length > 0) {
        // 显示加载状态
        $chartContainer.html('<div class="text-center p-4"><div class="loading-spinner"></div> 加载中...</div>');
        
        // 重新加载图表数据
        setTimeout(function() {
            if (typeof window[`load${chartType.charAt(0).toUpperCase() + chartType.slice(1)}Chart`] === 'function') {
                window[`load${chartType.charAt(0).toUpperCase() + chartType.slice(1)}Chart`]();
            }
        }, 1000);
    }
}

// 更新系统状态
function updateSystemStatus() {
    $.get('/api/scheduler-status')
        .done(function(data) {
            updateStatusIndicator('scheduler', data.running ? 'success' : 'error');
            $('#last-update-time').text(new Date().toLocaleString('zh-CN'));
            
            // 更新状态文本
            const statusText = data.running ? '系统运行正常' : '系统异常';
            $('.navbar-text').html(`<span class="status-indicator status-${data.running ? 'success' : 'error'}"></span>${statusText}`);
        })
        .fail(function() {
            updateStatusIndicator('scheduler', 'error');
            $('.navbar-text').html('<span class="status-indicator status-error"></span>系统连接异常');
        });
}

// 更新状态指示器
function updateStatusIndicator(component, status) {
    const $indicator = $(`.status-indicator[data-component="${component}"]`);
    $indicator.removeClass('status-success status-warning status-error')
             .addClass(`status-${status}`);
}

// 更新数据统计
function updateDataStatistics() {
    // 更新种子数据统计
    $.get('/api/seed-prices?limit=1')
        .done(function(data) {
            const count = Array.isArray(data) ? data.length : (data.total || 0);
            $('#seed-count').text(formatNumber(count));
        });
    
    // 更新天气数据统计
    $.get('/api/weather-forecast?limit=1')
        .done(function(data) {
            const count = Array.isArray(data) ? data.length : (data.total || 0);
            $('#weather-count').text(formatNumber(count));
        });
    
    // 更新农机数据统计
    $.get('/api/farm-machines?limit=1')
        .done(function(data) {
            const count = Array.isArray(data) ? data.length : (data.total || 0);
            $('#machine-count').text(formatNumber(count));
        });
}

// 初始化数据表格
function initializeDataTables() {
    if (typeof $.fn.DataTable !== 'undefined') {
        $('.data-table table').DataTable({
            language: {
                url: '//cdn.datatables.net/plug-ins/1.11.5/i18n/zh.json'
            },
            responsive: true,
            pageLength: 10,
            order: [[0, 'desc']]
        });
    }
}

// 获取网站名称
function getWebsiteName(website) {
    const names = {
        'seed_trade': '中国种子交易网',
        'weather': '中国天气网',
        'farm_machine': '农机360网'
    };
    return names[website] || website;
}

// 根据网站获取数据类型
function getDataTypeFromWebsite(website) {
    const types = {
        'seed_trade': 'seed_prices',
        'weather': 'weather',
        'farm_machine': 'farm_machines'
    };
    return types[website] || website;
}

// 格式化数字
function formatNumber(num) {
    if (typeof num !== 'number') return '0';
    return new Intl.NumberFormat('zh-CN').format(num);
}

// 格式化价格
function formatPrice(price) {
    if (typeof price !== 'number') return '¥0.00';
    return '¥' + formatNumber(price.toFixed(2));
}

// 格式化日期
function formatDate(dateString) {
    if (!dateString) return '';
    const date = new Date(dateString);
    return date.toLocaleDateString('zh-CN');
}

// 格式化日期时间
function formatDateTime(dateString) {
    if (!dateString) return '';
    const date = new Date(dateString);
    return date.toLocaleString('zh-CN');
}

// 复制到剪贴板
function copyToClipboard(text) {
    if (navigator.clipboard) {
        navigator.clipboard.writeText(text).then(function() {
            showNotification('已复制到剪贴板', 'success', 2000);
        });
    } else {
        // 降级方案
        const textArea = document.createElement('textarea');
        textArea.value = text;
        document.body.appendChild(textArea);
        textArea.select();
        document.execCommand('copy');
        document.body.removeChild(textArea);
        showNotification('已复制到剪贴板', 'success', 2000);
    }
}

// 导出数据
function exportData(type, format = 'csv') {
    const url = `/api/export-${type}?format=${format}`;
    window.open(url, '_blank');
    showNotification(`正在导出${type}数据...`, 'info');
}

// 页面加载完成后的初始化
window.addEventListener('load', function() {
    // 延迟加载图表
    setTimeout(function() {
        if (typeof loadCharts === 'function') {
            loadCharts();
        }
    }, 500);
    
    // 初始化数据统计
    updateDataStatistics();
});

// 处理网络错误
window.addEventListener('online', function() {
    showNotification('网络连接已恢复', 'success');
    updateSystemStatus();
});

window.addEventListener('offline', function() {
    showNotification('网络连接已断开', 'warning');
});
