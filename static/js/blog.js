{
  const blogElement = document.querySelector(".blog");
  const rootStyles = getComputedStyle(blogElement);
  const colors = [
    rootStyles.getPropertyValue("--post-card-bg-1").trim(),
    rootStyles.getPropertyValue("--post-card-bg-2").trim(),
    rootStyles.getPropertyValue("--post-card-bg-3").trim(),
    rootStyles.getPropertyValue("--post-card-bg-4").trim(),
    rootStyles.getPropertyValue("--post-card-bg-5").trim(),
    rootStyles.getPropertyValue("--post-card-bg-6").trim(),
  ];

  const posts = document.querySelectorAll(".post");
  posts.forEach((post, idx) => {
    post.style.backgroundColor = colors[idx % colors.length];
  });
}
