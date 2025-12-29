// 点赞/取消点赞功能（修复二次操作问题）
function likeMovie(movieId) {
    const btn = document.getElementById(`like-btn-${movieId}`);
    // 防止重复点击（可选，优化体验）
    if (btn.dataset.loading) return;
    btn.dataset.loading = true;

    const csrfToken = document.querySelector('meta[name="csrf-token"]').content;
    // 精准判断按钮当前状态
    const isLiked = btn.innerText.trim() === '已点赞';
    // 动态切换请求地址
    const url = isLiked ? `/unlike/${movieId}` : `/like/${movieId}`;

    fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken
        }
    })
    .then(response => {
        if (!response.ok) throw new Error(`HTTP错误：${response.status}`);
        return response.json();
    })
    .then(data => {
        if (data.success) {
            // 1. 动态更新按钮文本
            btn.innerText = isLiked ? '点赞该影片' : '已点赞';
            // 2. 动态控制禁用状态（核心修复：取消点赞后启用，点赞后无需禁用）
            // 移除固定禁用，改为可选（若需禁用点赞后按钮，取消点赞时必须恢复启用）
            btn.disabled = !isLiked; // 点赞后：disabled=true；取消点赞后：disabled=false
        }
        alert(data.msg);
    })
    .catch(error => {
        console.error('操作失败：', error);
        alert('网络错误，操作失败');
    })
    .finally(() => {
        // 移除加载状态，允许再次点击
        delete btn.dataset.loading;
    });
}
