// static/scripts.js
document.querySelectorAll('.btn-like').forEach(button => {
    button.addEventListener('click', async (e) => {
      e.preventDefault();
      const response = await fetch(e.target.form.action, { method: 'POST' });
      if (response.ok) {
        location.reload(); // 或更新点赞数
      }
    });
  });