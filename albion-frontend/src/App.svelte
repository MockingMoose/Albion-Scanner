<script>
  let results = /** @type {Array<{base_name:string, target_name:string, profit:number, city:String, base_icon:string}>} */ ([]);
  let premium = false;

  let cities = [
    { name: "Bridgewatch", checked: false },
    { name: "Martlock", checked: false },
    { name: "Fort Sterling", checked: false },
    { name: "Lymhurst", checked: false },
    { name: "Thetford", checked: false },
    { name: "Caerleon", checked: false }
  ];

  async function loadData() {
    console.log("Fetching profits.json...");
    const res = await fetch("/profits.json");
    results = await res.json();
    console.log("Loaded results:", results);
  }

  function toggleCheck(city) {
    city.checked = !city.checked;
    cities = [...cities];
  }

  function scanData() {
    // call backend
  }

  loadData();
</script>

<style>
* {
  font-family: sans-serif;
}
  table {
    width: 100%;
    border-collapse: collapse;
    margin-top: 20px;
  }

  th, td {
    border: 1px solid #ccc;
    padding: 8px;
  }

  img {
    width: 100px;
    height: 100px;
    object-fit: contain;
    image-rendering: crisp-edges;
  }
  #profit {
    color: greenyellow;
  }
  /* Page layout */
.container {
  width: 100%;
  max-width: 900px;
  margin: 0 auto;
  padding: 20px;
  display: flex;
  flex-direction: column;
  gap: 20px;
  font-family: sans-serif;
}

/* City grid */
.city-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr); /* 3 columns */
  gap: 20px;
}

/* Each city block */
.city-card {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
}

.city {
  color: black,
}

.city-card button {
  width: 100%;
  padding: 12px;
  background: gold;
  border: 1px solid #ccc;
  border-radius: 6px;
  font-size: 16px;
  cursor: pointer;
}

.city-card button:hover {
  background: goldenrod;
}

/* Premium row */
.premium-row {
  display: flex;
  align-items: center;
  gap: 10px;
  font-size: 18px;
}

/* Scan button */
.scan-btn {
  padding: 15px;
  font-size: 18px;
  background: #4a8af4;
  color: white;
  border: none;
  border-radius: 6px;
  cursor: pointer;
}

.scan-btn:hover {
  background: #3a78d8;
}
</style>

<div class="container">

  <h1>Select Cities</h1>

  <div class="city-grid">
    {#each cities as city}
      <div class="city-card">
        <button class="city" on:click={() => toggleCheck(city)}>{city.name}</button>
        <input type="checkbox" bind:checked={city.checked} />
      </div>
    {/each}
  </div>

  <div class="premium-row">
    <label for="premium">Premium?</label>
    <input type="checkbox" name="premium" bind:checked={premium} />
  </div>

  <button class="scan-btn" on:click={scanData}>
    Scan Data
  </button>

</div>
<table>
  <thead>
    <tr>
      <th>Icon</th>
      <th>Item</th>
      <th>City</th>
      <th>Target</th>
      <th>Profit</th>
    </tr>
  </thead>

  <tbody>
    {#each results as r}
      <tr>
        <td>
          <img src={r.base_icon} width="100" height="100" alt={r.base_name}/>
        </td>
        <td>{r.base_name}</td>
        <td>{r.city}</td>
        <td>{r.target_name}</td>
        <td id="profit">{r.profit}</td>
      </tr>
    {/each}
  </tbody>
</table>