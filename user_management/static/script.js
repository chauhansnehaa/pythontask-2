document.addEventListener('DOMContentLoaded', function() {
  const postsContainer = document.getElementById('posts-list');
  const postItems = postsContainer.getElementsByClassName('post-item');

  Array.from(postItems).forEach(post => {
      // Apply styling using JavaScript
      post.style.background = '#f9f9f9';
      post.style.border = '1px solid #ddd';
      post.style.borderRadius = '8px';
      post.style.padding = '1rem';
      post.style.width = 'calc(33.333% - 1rem)';
      post.style.boxShadow = '0 2px 4px rgba(0,0,0,0.1)';
      post.style.transition = 'background-color 0.3s, box-shadow 0.3s';

      post.addEventListener('mouseover', () => {
          post.style.backgroundColor = '#fff';
          post.style.boxShadow = '0 4px 8px rgba(0,0,0,0.2)';
      });

      post.addEventListener('mouseout', () => {
          post.style.backgroundColor = '#f9f9f9';
          post.style.boxShadow = '0 2px 4px rgba(0,0,0,0.1)';
      });

      // Style the img element inside the post item
      const img = post.querySelector('img');
      if (img) {
          img.style.maxWidth = '100%';
          img.style.height = 'auto';
          img.style.borderRadius = '4px';
      }

      // Style the links inside the post item
      const links = post.querySelectorAll('a');
      links.forEach(link => {
          link.style.color = '#007bff';
          link.style.textDecoration = 'none';
          link.addEventListener('mouseover', () => {
              link.style.textDecoration = 'underline';
          });
          link.addEventListener('mouseout', () => {
              link.style.textDecoration = 'none';
          });
      });
  });
});
