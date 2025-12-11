document.addEventListener('DOMContentLoaded', function() {
    const header = document.getElementById('section-header');
    
    // スクロールを開始して背景を出現させる閾値 (5rem = 80px)
    const SCROLL_THRESHOLD = 80; 

    function handleScroll() {
        // 現在のスクロール量を取得
        const scrollPosition = window.scrollY; 

        if (scrollPosition > SCROLL_THRESHOLD) {
            // 閾値を超えたら .scrolled クラスを付与
            header.classList.add('scrolled');
        } else {
            // 閾値以下の場合はクラスを削除
            header.classList.remove('scrolled');
        }
    }

    // スクロールイベントが発生するたびに handleScroll 関数を実行
    window.addEventListener('scroll', handleScroll);
});



document.addEventListener("DOMContentLoaded", () => {
  const burger = document.querySelector(".hamburger");
  const nav = document.querySelector(".header-nav");

  burger.addEventListener("click", () => {
    burger.classList.toggle("active");
    nav.classList.toggle("active");
  });

  // メニュークリックで閉じる
  nav.querySelectorAll("a").forEach(link => {
    link.addEventListener("click", () => {
      burger.classList.remove("active");
      nav.classList.remove("active");
    });
  });
});
