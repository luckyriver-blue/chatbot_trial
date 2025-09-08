#送信後最下部へスクロールするJavascript
scroll_js = '''
<script>
    //スクロール位置を保持
    window.onload = function() {
        var savedScrollPosition = sessionStorage.getItem('scrollPosition');
        if (savedScrollPosition) {
            var target = parent.document.querySelector('section.st-emotion-cache-bm2z3a');
            if (target) {
                target.scrollTop = savedScrollPosition;
            }
        }
    }
    document.querySelectorAll("button").forEach((btn, i) => {
        console.log(i, btn.innerText, btn.getAttribute("data-testid"));
    });
    var sendButton = parent.document.querySelector('button[data-testid="stBaseButton-secondary"]');
    if (sendButton) {
        // ボタンのクリックイベントを監視
        
        sendButton.addEventListener('click', function() {
            // スクロール対象の要素を取得
            var target = parent.document.querySelector('section.st-emotion-cache-bm2z3a');

            if (target) {
                // スクロールを最下部に移動
                target.scrollTop = target.scrollHeight;
                sessionStorage.setItem('scrollPosition', target.scrollTop);
            } 
        });
    } 
</script>
'''