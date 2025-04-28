window.onload = () => {
  const ferrari = document.getElementById('ferrari');
  const article = document.getElementById('race-article');
  const audio = document.getElementById('f1Audio');
  const volumeButton = document.getElementById('volumeButton');
  let isMuted = false;

  // Ferrari animation
  ferrari.style.left = 'calc(100% + 200px)';

  // Play sound
  audio.currentTime = 0;
  audio.play().catch(err => {
    console.warn("Autoplay blocked:", err);
  });

  // Volume button
  volumeButton.addEventListener('click', () => {
    if (isMuted) {
      audio.play();
      volumeButton.textContent = '🔊';
    } else {
      audio.pause();
      volumeButton.textContent = '🔇';
    }
    isMuted = !isMuted;
  });

  // Show intro article after 6s
  setTimeout(() => {
    article.style.display = 'block';
  }, 4000);

  // Show About F1 Section after 10s
  setTimeout(() => {
    document.getElementById('aboutF1Section').style.display = 'block';
  }, 4250);
};

  
  wrapper.addEventListener("click", () => {
    const isVisible = driverDiv.style.display === "block";
    driverDiv.style.display = isVisible ? "none" : "block";
    wrapper.classList.toggle("expanded", !isVisible);
  });

  function countryToFlagEmoji(countryCode) {
    return countryCode
      .toUpperCase()
      .replace(/./g, char => String.fromCodePoint(127397 + char.charCodeAt()));
  }

  function toggleEdit(id) {
    const form = document.getElementById(`editForm-${id}`);
    form.style.display = form.style.display === 'none' ? 'block' : 'none';
  }
  
  function submitEdit(e, driverId) {
    e.preventDefault();
    const form = e.target;
    const data = Object.fromEntries(new FormData(form).entries());
  
    fetch(`/api/update-driver/${driverId}`, {
      method: "PUT",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(data)
    })
    .then(res => {
      if (res.ok) return res.json();
      else throw new Error("Failed to update driver");
    })
    .then(() => {
      alert("Driver updated!");
      return fetch("/api/drivers");
    })
    .then(res => res.json())
    .then(data => {
      allDrivers = data;
      renderDrivers(allDrivers);
    })
    .catch(err => alert("Error: " + err.message));
  }
  
  function formatDate(dateString) {
    const d = new Date(dateString);
    const year = d.getFullYear();
    const month = String(d.getMonth() + 1).padStart(2, '0');
    const day = String(d.getDate()).padStart(2, '0');
    return `${year}-${month}-${day}`;
  }
  
  function deleteDriver(driverId) {
    if (!confirm("Are you sure you want to delete this driver?")) return;
  
    fetch(`/api/delete-driver/${driverId}`, {
      method: "DELETE"
    })
      .then(res => {
        if (!res.ok) throw new Error("Failed to delete");
        alert("🗑️ Driver deleted!");
        return fetch("/api/drivers");
      })
      .then(res => res.json())
      .then(data => {
        allDrivers = data;
        renderDrivers(allDrivers);
      })
      .catch(err => alert("❌ Error: " + err.message));
  }
