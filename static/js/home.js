async function post(event) {
    event.preventDefault(); // フォームのデフォルトの送信を防ぐ
    const replyTo = event.currentTarget.dataset.replyto;
    const body = document.getElementById('postContent').value;
    const username = document.getElementById('username').value;
    const header = document.getElementById('headerContent').value;
    const fileInput = document.querySelector("input[type='file']");
    const file = fileInput.files[0];

    if (header.trim() === '' && body.trim() === '') {
      alert('投稿内容を入力してください。');
      return;
    }
    console.log("replyto," ,replyTo)
    console.log('header:', header);
    console.log('body:', body);
    console.log('Username:', username);
    console.log('File:', file);

    const formData = new FormData();
    formData.append('body', body);
    formData.append('username', username);
    formData.append('header', header);
    if (file) {
        formData.append('file', file);
    }
    if (replyTo){
        formData.append("replyto",replyTo)
    }
    try {
        const response = await fetch('/api/post', {
            method: 'POST',
            body: formData // FormDataを使用してマルチパートフォームデータを送信
        });

        if (response.ok) {
            const result = await response.json();
            console.log('投稿成功:', result);
            document.getElementById('postForm').reset();
        } else {
            const error = await response.json();
            console.error('投稿エラー:', error);
            alert('投稿に失敗しました。');
        }
    } catch (error) {
        console.error('ネットワークエラー:', error);
    }
    location.reload()
}



function post_delete(postId){
    event.preventDefault()

    fetch(`/api/post_delete/${postId}`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-Requested-With': 'XMLHttpRequest'
        },
        credentials: 'same-origin'
    })
    location.reload()
}

  function likePost(postId, userId) {
    fetch(`/api/like_post/${postId}/${userId}`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-Requested-With': 'XMLHttpRequest'
        },
        credentials: 'same-origin'
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            document.getElementById(`like-count-${postId}`).textContent = data.new_like_count;
        }
    })
    .catch(error => console.error('Error:', error));
    location.reload()
}


function go_someday(event){

    event.preventDefault()   
    
    const tagName = event.target.dataset.tag;
    const year = document.getElementById('year').value;
    const month = document.getElementById('month').value;
    const day = document.getElementById('day').value;
    
    if(tagName != null){
        window.location = `/home/${year}/${month}/${day}/${tagName}`
    }
    else{
        window.location = `/home/${year}/${month}/${day}`
    }
}

function copyPostLink(postId) {
    const link = `${window.location.origin}/post/${postId}`;

    navigator.clipboard.writeText(link)
        .then(() => {
            alert("リンクをコピーしました！");
        })
        .catch(err => {
            console.error('コピーに失敗しました:', err);
            alert("コピーに失敗しました。手動でコピーしてください。");
        });
}

