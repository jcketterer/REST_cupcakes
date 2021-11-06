const BASE_URL = 'http://127.0.0.1:5000/api';

function genCupcakeHTML(cupcake) {
  return `
    <div data-cupcake-id=${cupcake.id}>
      <li>
        ${cupcake.flavor} / ${cupcake.size} / ${cupcake.rating}
        <button class="btn btn-danger btn-small delete-button">X</button>
      </li>
      <img class="Cupcake-image"
            src="${cupcake.image}"
            alt="(no image provided)">
    </div>
  `;
}

async function showCupcakes() {
  const res = await axios.get(`${BASE_URL}/cupcakes`);
  console.log(res);

  for (let cupcakeData of res.data.cupcakes) {
    let newCupcake = $(genCupcakeHTML(cupcakeData));
    $('#cupcake-list').append(newCupcake);
  }
}

$('#new-cupcake-form').on('submit', async function (e) {
  e.preventDefault();

  let flavor = $('#form-flavor').val();
  let rating = $('#form-rating').val();
  let size = $('#form-size').val();
  let image = $('#form-image').val();

  const newCupcakeResp = await axios.post(`${BASE_URL}/cupcakes`, {
    flavor,
    rating,
    size,
    image,
  });

  let newCupcake = $(gen_cupcakeHTML(newCupcakeResp.data.cupcake));
  $('#cupcake-list').append(newCupcake);
  $('#new-cupcake-form').trigger('reset');
});

$('#cupcake-list').on('click', '.delete-button', async function (e) {
  e.preventDefault();

  let $cupcake = $(e.target).closest('div');
  let cupcakeId = $cupcake.attr('data-cupcake-id');

  await axios.delete(`${BASE_URL}/cupcakes/${cupcakeId}`);
  $cupcake.remove();
});

$(showCupcakes);
