function post(event) {
    event.preventDefault(); // フォームのデフォルトの送信を防ぐ
  
    const body = document.getElementById('postContent').value;
    const username = document.getElementById('username').value;
    const header = document.getElementById('headerContent').value;
    

    if (header.trim() === '' && header.trim === '') {
      alert('投稿内容を入力してください。');
      return;
    }
  
    console.log('header:', header);
    console.log('body:',body)
    console.log('Username:', username);

    fetch('/api/post',{method: 'POST',headers: {
        'Content-Type' : 'application/json',
    },body: JSON.stringify({
        body,username,header})
    })
    document.getElementById('postForm').reset();
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

