function saveOfflineData(key, data) {
    const request = indexedDB.open("appEntrenamientoDB", 1);
    request.onupgradeneeded = () => {
        request.result.createObjectStore("data");
    };
    request.onsuccess = () => {
        const db = request.result;
        const tx = db.transaction("data", "readwrite");
        tx.objectStore("data").put(data, key);
    };
}

function loadOfflineData(key, callback) {
    const request = indexedDB.open("appEntrenamientoDB", 1);
    request.onupgradeneeded = () => {
        request.result.createObjectStore("data");
    };
    request.onsuccess = () => {
        const db = request.result;
        const tx = db.transaction("data", "readonly");
        const getReq = tx.objectStore("data").get(key);
        getReq.onsuccess = () => callback(getReq.result);
    };
}