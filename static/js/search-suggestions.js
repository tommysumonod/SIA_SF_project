const input = document.getElementById("search-input");
const clearBtn = document.getElementById("clear-btn");
const suggestions = document.getElementById("suggestions");

// Example data for suggestions
const data = ["Crafts", "Gallery", "Create", "About", "Showcase"];

input.addEventListener("input", () => {
  const value = input.value.trim();
  suggestions.innerHTML = "";

  if (value.length > 0) {
    clearBtn.style.display = "block";
    const filtered = data.filter(item =>
      item.toLowerCase().includes(value.toLowerCase())
    );

    filtered.forEach(item => {
      const li = document.createElement("li");
      li.textContent = item;
      li.addEventListener("click", () => {
        input.value = item;
        suggestions.style.display = "none";
        clearBtn.style.display = "block";
      });
      suggestions.appendChild(li);
    });

    suggestions.style.display = filtered.length > 0 ? "block" : "none";
  } else {
    suggestions.style.display = "none";
    clearBtn.style.display = "none";
  }
});

clearBtn.addEventListener("click", () => {
  input.value = "";
  suggestions.style.display = "none";
  clearBtn.style.display = "none";
});


