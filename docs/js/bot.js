document.addEventListener("DOMContentLoaded", () => {
    // 创建一个半透明背景层
    var overlay = document.createElement('div');
    overlay.id = 'overlay';
    overlay.style.display = 'none';  // 初始状态隐藏
    overlay.style.position = 'fixed';
    overlay.style.top = 0;
    overlay.style.left = 0;
    overlay.style.width = '100%';
    overlay.style.height = '100%';
    overlay.style.backgroundColor = 'rgba(0, 0, 0, 0.5)';
    overlay.style.zIndex = 9998;
    document.body.appendChild(overlay);
  
    // 创建一个 Streamlit iframe
    var iframe = document.createElement('iframe');
    iframe.src = 'http://localhost:8501';
    iframe.id = 'streamlit-iframe';
    iframe.style.display = 'none';  // 初始状态隐藏
    iframe.style.position = 'fixed';
    iframe.style.top = '50%';
    iframe.style.left = '50%';
    iframe.style.width = '800px';
    iframe.style.height = '600px';
    iframe.style.border = '1px solid #ccc';
    iframe.style.borderRadius = '10px';
    iframe.style.transform = 'translate(-50%, -50%)';
    iframe.style.zIndex = 9999;
    document.body.appendChild(iframe);
  
    // 创建一个机器人按钮
    var button = document.createElement('button');
    button.id = 'chatbot-button';
    button.textContent = '🐈';
    button.style.position = 'fixed';
    button.style.bottom = '60px';
    button.style.right = '60px';
    button.style.width = '80px';
    button.style.height = '80px';
    button.style.backgroundColor = '#010810';
    button.style.color = '#ffffff';
    button.style.border = 'none';
    button.style.borderRadius = '50%';
    button.style.fontSize = '40px';
    button.style.display = 'flex';
    button.style.alignItems = 'center';
    button.style.justifyContent = 'center';
    button.style.cursor = 'pointer';
    button.style.zIndex = 10000;
    document.body.appendChild(button);
  
    // 点击按钮时切换 iframe 和 overlay 的显示/隐藏
    button.addEventListener('click', function(event) {
      event.stopPropagation();  // 阻止事件冒泡
      if (iframe.style.display === 'none') {
        iframe.style.display = 'block';
        overlay.style.display = 'block';
      } else {
        iframe.style.display = 'none';
        overlay.style.display = 'none';
      }
    });
  
    // 点击 overlay 时隐藏 iframe 和 overlay
    overlay.addEventListener('click', function() {
      iframe.style.display = 'none';
      overlay.style.display = 'none';
    });
  });