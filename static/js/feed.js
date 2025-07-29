document.addEventListener("DOMContentLoaded", () => {
  document.querySelectorAll(".like-form").forEach(form => {
    form.addEventListener("submit", async (e) => {
      e.preventDefault();
      const postId = form.dataset.postId;
      const response = await fetch(`/post/${postId}/like/`, {
        method: "POST",
        headers: {
          "X-CSRFToken": form.querySelector("[name=csrfmiddlewaretoken]").value
        }
      });
      const data = await response.json();
      form.querySelector(".like-btn").textContent = data.liked ? "❤️" : "🤍";
      form.querySelector(".likes-count").textContent = `${data.likes_count} Likes`;
    });
  });

  document.querySelectorAll(".comment-form").forEach(form => {
    form.addEventListener("submit", async (e) => {
      e.preventDefault();
      const postId = form.dataset.postId;
      const commentBox = form.querySelector("input[name=comment]");
      const response = await fetch(`/post/${postId}/comment/`, {
        method: "POST",
        headers: {
          "X-CSRFToken": form.querySelector("[name=csrfmiddlewaretoken]").value,
          "Content-Type": "application/x-www-form-urlencoded"
        },
        body: `comment=${encodeURIComponent(commentBox.value)}`
      });
      const data = await response.json();
      document.querySelector(`#comments-${postId}`).innerHTML = data.comments_html;
      commentBox.value = "";
    });
  });
});
