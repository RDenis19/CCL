  document.addEventListener('DOMContentLoaded', function () {
    const rows = document.querySelectorAll('tbody tr');
    rows.forEach((row, index) => {
      row.style.opacity = '0';
      row.style.transform = 'translateY(15px)';
      row.style.transition = 'opacity 0.4s ease-out, transform 0.4s ease-out';
      setTimeout(() => {
        row.style.opacity = '1';
        row.style.transform = 'translateY(0)';
      }, 100 * index);
    });
  });