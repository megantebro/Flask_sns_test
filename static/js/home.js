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
  