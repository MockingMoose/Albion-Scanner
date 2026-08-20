<script>
  let results = /** @type {Array<{base_name:string, target_name:string, profit:number, base_icon:string}>} */ ([]);

  async function loadData() {
    console.log("Fetching profits.json...");
    const res = await fetch("/profits.json");
    results = await res.json();
    console.log("Loaded results:", results);
  }
  loadData();
</script>
<style>
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
</style>

<table>
  <thead>
    <tr>
      <th>Icon</th>
      <th>Item</th>
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
        <td>{r.target_name}</td>
        <td id="profit">{r.profit}</td>
      </tr>
    {/each}
  </tbody>
</table>