/* pyscript.js - Pygame 遊戲啟動腳本 */

function ready() {
    var canvas = document.getElementById('pygame-canvas');
    if (!canvas) {
        console.error("錯誤：找不到 ID 為 'pygame-canvas' 的元素。");
        return;
    }
    
    var config = {
        canvas: canvas, 
        // 指定運行您的遊戲主程式
        main: 'main.py', 
        title: '點數字 — Pygame 小遊戲',
        // 確保寬高與 main.py 內部設定（600x600）一致，或在 main.py 中改為 800x600
        width: 600,  
        height: 600,
        mounts: [],
        
        ume_onload: function() {
            console.log("Pygbag UME 核心載入完成，等待使用者點擊開始按鈕...");
        }
    };
    
    // 啟動 Pygbag 引擎
    window.MM.ume_init(config);
}

window.addEventListener('load', ready);