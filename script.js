// Initial data
const HTML_CODE = (
    `<div class="p-4">
       <div class="alert alert-warning" role="alert">
          Bootstrap 5 CSS injected
       </div>
    
       <div class="card">
          <div class="card-body">
             <h5 class="card-title">Special title treatment</h5>
             <p class="card-text">With supporting text below as a natural lead-in to additional content.</p>
             <a href="#" class="btn btn-primary">Go somewhere</a>
          </div>
       </div>
    </div>
    `);
    const CSS_LINKS = [`https://cdn.jsdelivr.net/npm/bootstrap/dist/css/bootstrap.min.css`];
    
    // Elements
    const editorCode = document.getElementById("editorCode");
    const editorPreview = document.getElementById('editorPreview').contentWindow.document;
    const editorCopyButton = document.getElementById('editorCopyClipboard');
    
    // <iframe> inject CSS
    CSS_LINKS.forEach(linkURL => {
       const link = document.createElement('link');
       link.href = linkURL;
       link.rel = "stylesheet";
       editorPreview.head.appendChild(link);
    })
    
    // Monaco loader
    require.config({
       paths: { vs: "https://cdn.jsdelivr.net/npm/monaco-editor/min/vs" }
    });
    
    window.MonacoEnvironment = {
       getWorkerUrl: function(workerId, label) {
          return `data:text/javascript;charset=utf-8,${encodeURIComponent(`
            self.MonacoEnvironment = {
              baseUrl: 'https://cdn.jsdelivr.net/npm/monaco-editor/min/'
            };
            importScripts('https://cdn.jsdelivr.net/npm/monaco-editor/min/vs/base/worker/workerMain.js');`)}`;
       }
    };
    
    // Monaco init
    require(["vs/editor/editor.main"], function() {
       createEditor(editorCode);
    });
    
    function createEditor(editorContainer) {
       let editor = monaco.editor.create(editorContainer, {
          value: HTML_CODE,
          language: "html",
          minimap: { enabled: false },
          automaticLayout: true,
          contextmenu: false,
          fontSize: 12,
          scrollbar: {
             useShadows: false,
             vertical: "visible",
             horizontal: "visible",
             horizontalScrollbarSize: 12,
             verticalScrollbarSize: 12
          }
       });
       
       editorPreview.body.innerHTML = HTML_CODE;
    
       editor.onDidChangeModelContent(() => {
          editorPreview.body.innerHTML = editor.getValue();
       });
       
       editorCopyButton.onclick = () => {
          copyToClipboard(editor.getValue());
          const editorCopyButtonText = editorCopyButton.innerHTML;
          editorCopyButton.innerHTML = "Copied!";
          editorCopyButton.disabled = true;
          setTimeout(() => {
             editorCopyButton.disabled = false;
             editorCopyButton.innerHTML = editorCopyButtonText
          }, 500);
       }
    }
    
    function copyToClipboard(str) {
       const el = document.createElement("textarea");
       el.value = str;
       document.body.appendChild(el);
       el.select();
       document.execCommand("copy");
       document.body.removeChild(el);
    }
    
    