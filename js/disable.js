changeTitle = () => {
  window.onblur = () => {
    document.title = "Neurobits";
  };
};

hiddenToggle = () => {
  let toggle = document.getElementsByClassName('theme-switch');
  toggle[0].style.display = "none";
};

setDarkTheme = () => {
  const currentTheme = window.localStorage && window.localStorage.getItem('theme')
  const isDark = currentTheme === 'dark'
  if (! isDark) {
    document.body.classList.add('dark-theme')
    window.localStorage &&
      window.localStorage.setItem('theme', document.body.classList.contains('dark-theme') ? 'dark' : '', )
  };
};


hiddenToggle();
changeTitle();
setDarkTheme();