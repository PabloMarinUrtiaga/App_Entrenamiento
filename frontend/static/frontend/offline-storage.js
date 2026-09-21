const DB_VERSION = 2;

function openDB(callback) {
    const request = indexedDB.open("appEntrenamientoDB", DB_VERSION);
    request.onupgradeneeded = (e) => {
        const db = e.target.result;
        if (!db.objectStoreNames.contains("data")) db.createObjectStore("data");
        if (!db.objectStoreNames.contains("pendingResults")) {
            db.createObjectStore("pendingResults", { autoIncrement: true });
        }
    };
    request.onsuccess = () => callback(request.result);
}

function saveOfflineData(key, data) {
    openDB((db) => {
        const tx = db.transaction("data", "readwrite");
        tx.objectStore("data").put(data, key);
    });
}

function loadOfflineData(key, callback) {
    openDB((db) => {
        const tx = db.transaction("data", "readonly");
        const getReq = tx.objectStore("data").get(key);
        getReq.onsuccess = () => callback(getReq.result);
    });
}

function queueOfflineResult(url, dataObj) {
    openDB((db) => {
        const tx = db.transaction("pendingResults", "readwrite");
        tx.objectStore("pendingResults").add({ url, data: dataObj });
    });
}

function syncPendingResults() {
    openDB((db) => {
        const tx = db.transaction("pendingResults", "readwrite");
        const store = tx.objectStore("pendingResults");
        store.openCursor().onsuccess = (event) => {
            const cursor = event.target.result;
            if (!cursor) return;
            const { url, data } = cursor.value;
            const formData = new FormData();
            Object.entries(data).forEach(([key, value]) => formData.append(key, value));

            fetch(url, { method: "POST", body: formData, credentials: "same-origin" })
                .then((res) => {
                    if (res.ok || res.redirected) cursor.delete();
                })
                .catch(() => {}); // sigue sin conexión, se reintenta la próxima vez

            cursor.continue();
        };
    });
}

window.addEventListener("online", syncPendingResults);
document.addEventListener("DOMContentLoaded", syncPendingResults);