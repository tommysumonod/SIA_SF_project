// upload-comments.js - handles AJAX posting of comments and simple UI updates
(function(){
  function getCookie(name){
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
  }

  const form = document.getElementById('commentForm');
  const list = document.getElementById('commentsList');
  if (!form || !list) return;

  form.addEventListener('submit', async (e) => {
    e.preventDefault();
    const text = document.getElementById('commentText').value.trim();
    if (!text) return;

    const csrf = getCookie('csrftoken');
    const action = form.getAttribute('action');
    const payload = new FormData();
    payload.append('comment', text);

    const resp = await fetch(action, { method:'POST', headers: {'X-CSRFToken': csrf}, body: payload });
    const json = await resp.json();
    if (json.success){
      // append comment to list
      const div = document.createElement('div');
      div.className = 'comment-item';
      div.innerHTML = `<a href="/profile/?uid=${json.user_uid}" class="comment-author"><img src="${json.profile_pic}" class="comment-avatar"><span class="comment-name">${json.name}</span></a><div class="comment-body"><p>${json.comment}</p><div class="comment-ts">just now</div></div>`;
      list.appendChild(div);
      list.scrollTop = list.scrollHeight;
      document.getElementById('commentText').value = '';
    } else {
      alert('Failed to post comment: ' + (json.error || 'unknown'));
    }
  });
})();
