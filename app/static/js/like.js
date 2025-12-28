// 点赞功能
function likeMovie(movieId) {
    const btn = document.getElementById(`like-btn-${movieId}`);
    // 恢复：获取CSRF令牌
    const csrfToken = document.querySelector('meta[name="csrf-token"]').content;

    fetch(`/like/${movieId}`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            // 恢复：携带CSRF令牌
            'X-CSRFToken': csrfToken
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            btn.innerText = '已点赞';
            btn.disabled = true;
            alert(data.msg);
        } else {
            alert(data.msg);
        }
    })
    .catch(error => {
        console.error('点赞请求失败：', error);
        alert('网络错误，点赞失败');
    });
}
