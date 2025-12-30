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


// 通用AJAX点赞函数

function likeMovieAjax(movieId) {

    const btn = document.getElementById(`like-btn-${movieId}`);

    const likeCountElement = document.querySelector(`.like-count-${movieId}`);

    const csrfToken = document.querySelector('meta[name="csrf-token"]').content;


    const originalText = btn.innerHTML;

    const originalDisabled = btn.disabled;



    // 显示加载状态

    btn.disabled = true;

    btn.innerHTML = '处理中...';


    fetch(`/like/${movieId}`, {

        method: 'POST',

        headers: {

            'Content-Type': 'application/json',

            'X-CSRFToken': csrfToken

        }

    })

    .then(response => response.json())

    .then(data => {

        if (data.success) {

            if (data.liked) {

                btn.innerHTML = '❤️ 已点赞';

                btn.dataset.liked = 'true';

                btn.disabled = true;

            } else {

                btn.innerHTML = '💙 点赞';

                btn.dataset.liked = 'false';

                btn.disabled = false;

            }



            // 更新点赞数

            if (likeCountElement && data.likes_count !== undefined) {

                likeCountElement.textContent = `(${data.likes_count} 人点赞)`;

            }

        } else {

            alert(data.msg || '操作失败，请重试。');

            btn.innerHTML = originalText;

            btn.disabled = originalDisabled;

        }

    })

    .catch(error => {

        console.error('点赞请求失败：', error);

        alert('网络错误，点赞失败');

        btn.innerHTML = originalText;

        btn.disabled = originalDisabled;

    });

}
