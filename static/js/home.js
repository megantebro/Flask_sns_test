async function post(event) {
    event.preventDefault(); // フォームのデフォルトの送信を防ぐ
  
    const body = document.getElementById('postContent').value;
    const username = document.getElementById('username').value;
    const header = document.getElementById('headerContent').value;
    const fileInput = document.querySelector("input[type='file']");
    const file = fileInput.files[0];

    if (header.trim() === '' && body.trim() === '') {
      alert('投稿内容を入力してください。');
      return;
    }
    
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
}


function go_someday(event){
   
    event.preventDefault()   
    const year = document.getElementById('year').value;
    const month = document.getElementById('month').value;
    const day = document.getElementById('day').value;
    window.location = `/home/${year}/${month}/${day}`
}

