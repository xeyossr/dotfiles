async function getRequest(url = '') {
  const response = await fetch(url, {
      method: 'GET',
      cache: 'no-cache'
  })
  return response.json()
}
document.addEventListener('DOMContentLoaded', function () {
  let url = document.location
  let route = "/flaskwebgui-keep-server-alive"
  let interval_request = 3 * 1000 //sec
  function keep_alive_server() {
      getRequest(url + route)
          .then(data => console.log(data))
  }
  setInterval(keep_alive_server, interval_request)()
})




// Popup aç/kapa işlevleri
function openPopup() {
    document.getElementById("popupForm").style.display = "block";
}

 function closePopup() {
    document.getElementById("popupForm").style.display = "none";
}

 // Task'ı formdan gönder
function submitForm(event) {
    event.preventDefault();

     let formData = new FormData(document.getElementById('taskForm'));

     // Bilgileri backend'e POST etmek için fetch kullanıyoruz
    fetch('/submit', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === 'success') {
            closePopup();
            // Task'ları yeniden yükle
            loadTasks();
        } else {
            alert("Bir hata oluştu.");
        }
    })
    .catch(error => {
        console.error('Hata:', error);
    });
}


document.addEventListener('click', function(event) {
    if (event.target.classList.contains('delete-button')) {
        const taskDiv = event.target.parentElement; // Div’i seç
        const taskId = event.target.getAttribute('data-id');

         // Silme isteği gönder
        fetch('/delete', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ id: taskId }),
        })
        .then(response => response.json())
        .then(data => {
            if (data.status === 'success') {
                // Silinen öğeyi arayüzden kaldır
                taskDiv.style.transition = 'opacity 0.5s'; // Yavaşça kaybolması için geçiş ekle
                taskDiv.style.opacity = '0'; // Opaklığı sıfıra düşür

                 // Geçiş sonrası div’i kaldır
                setTimeout(() => {
                    taskDiv.remove();
                }, 500); // 0.5 saniye bekle
            } else {
                console.error(data.message);
            }
        });
    }
});



// Edit 
let taskId;
// Edit button click event
document.addEventListener('click', function(event) {
    if (event.target.classList.contains('edit-button')) {
        const taskDiv = event.target.parentElement; // Div’i seç
        const taskId_str = event.target.getAttribute('data-id');
        taskId = Number(taskId_str)

        // data.json'dan verileri çek
        fetch('/data.json')
            .then(response => response.json())
            .then(data => {
                const task = data.find(item => item.id === taskId);
                if (task) {
                    // Formu doldur
                    document.getElementById('edit_name').value = task.name;
                    document.getElementById('edit_description').value = task.description;
                    document.getElementById('edit_image_url').value = task.image_url;
                    document.getElementById('edit_when').value = task.when;
                    document.getElementById('edit_time').value = task.time;

                    // Edit popup'ı göster
                    document.getElementById('editPopupForm').showModal();
                }
            })
            .catch(error => console.error('Error fetching data:', error));
    }
});

// Edit form submit event
function submitEditForm(event) {
    event.preventDefault(); // Formun varsayılan gönderimini engelle    
    console.log(taskId)
    const editedTask = {
        id: taskId,
        name: document.getElementById('edit_name').value,
        description: document.getElementById('edit_description').value,
        image_url: document.getElementById('edit_image_url').value,
        when: document.getElementById('edit_when').value,
        time: document.getElementById('edit_time').value,
    };

    // Güncelleme isteği gönder
    fetch('/edit-task', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(editedTask),
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === 'success') {
            // Başarılı güncelleme sonrası popup'ı kapat
            closeEditPopup();
            // Arayüzde güncellenmiş verileri göster (gerekirse burada güncellemeleri yap)
            loadTasks();
        } else {
            console.error(data.message);
        }
    })
    .catch(error => console.error('Error updating task:', error));
}

// Edit popup'ı kapatma fonksiyonu
function closeEditPopup() {
    document.getElementById('editPopupForm').close();
}







   // Tüm task'ları listeleyen fonksiyon
function loadTasks() {
    fetch('/tasks')
    .then(response => response.json())
    .then(tasks => {
        const taskContainer = document.getElementById("taskContainer");
        taskContainer.innerHTML = ""; // Mevcut içerikleri temizle
        tasks.forEach(task => {
            // Her task için yeni bir div oluşturuyoruz
            const taskDiv = document.createElement("div");
            taskDiv.classList.add("task-box");
            taskDiv.innerHTML = `
                <div class="task-info" data-id="${task.id}">
                    <img src="${task.image_url}" class="task-image" alt="Task Image" width="100" height="100">
                    <div class="task-details">
                        <h3>${task.name}</h3>
                        <p>${task.description}</p>
                        <span>${task.when} - ${task.time}</span>
                    </div>
                    <button class="delete-button" role="button" data-id="${task.id}"><i class="fa fa-trash" aria-hidden="true"></i></button>
                    <button class="edit-button" role="button" data-id="${task.id}"><i class="fa fa-pencil" aria-hidden="true"></i></button>  
                </div>
            `;
            taskContainer.appendChild(taskDiv);
        });
    })
    .catch(error => {
        console.error('Hata:', error);
    });
}






let clickedElement; // Sağ tık yapılan elementi saklamak için
let clickedElementDataId;


document.addEventListener('contextmenu', function(e) {
  e.preventDefault(); // Varsayılan sağ tık menüsünü engelle
  const menu = document.getElementById('custom-context-menu');
  clickedElement = this;
  //clickedElementDataId = Number(clickedElement.getAttribute('data-id'));
  console.log(clickedElement);
  menu.style.display = 'block';
  menu.style.zIndex = '999999999';
  menu.style.left = e.pageX + 'px'; // Sağ tık konumunu ayarla
  menu.style.top = e.pageY + 'px';
});

// Sağ tık menüsüne tıklanıldığında gizleme
window.addEventListener('click', function() {
  const menu = document.getElementById('custom-context-menu');
  menu.style.display = 'none'; // Menü gizle
});





/*function deleterightclick() {
      fetch('/delete', {
          method: 'POST',
          headers: {
              'Content-Type': 'application/json',
          },
          body: JSON.stringify({ id: clickedElementDataId }),
      })
      .then(response => response.json())
      .then(data => {
          if (data.status === 'success') {
              // Silinen öğeyi arayüzden kaldır
              taskDiv.style.transition = 'opacity 0.5s'; // Yavaşça kaybolması için geçiş ekle
              taskDiv.style.opacity = '0'; // Opaklığı sıfıra düşür

               // Geçiş sonrası div’i kaldır
              setTimeout(() => {
                  taskDiv.remove();
              }, 500); // 0.5 saniye bekle
          } else {
              console.error(data.message);
          }
      });
  }*/



/*
// Popup aç/kapa işlevleri
function openPopup() {
    document.getElementById("popupOverlay").style.display = "block";
    document.getElementById("popupForm").style.display = "block";
}

function closePopup() {
    document.getElementById("popupForm").style.animation = "slideOut 0.5s forwards"; // Kapanma animasyonu
    setTimeout(() => {
        document.getElementById("popupForm").style.display = "none";
        document.getElementById("popupOverlay").style.display = "none"; // Arka planı gizle
    }, 500); // Animasyon süresi
}

*/

function showPopup() {
    document.getElementById('popupForm').showModal();
    document.getElementById("popupForm").style.display = "block";
    document.getElementById('popupOverlay').style.display = 'block';
}

function closePopup() {
    document.getElementById('popupForm').close();
    document.getElementById("popupForm").style.display = "none";
    document.getElementById('popupOverlay').style.display = 'none';
}


 // Sayfa yüklendiğinde task'ları yükle
window.onload = loadTasks;