
Vue.component('evo-drawing', {
  props: ['drawing'],
  template:"#evodrawing-template",
  delimiters: ['[[', ']]'],
  computed: {
      rating_text: function () {
          if (this.current_rating == 0)
                return "Rate this";
          else
                return this.current_rating.toString() + " stars";

    }
    },
  data:function () {
    return {
      current_rating: 0
    }
  },
  methods:
        {
            public: function (event) {
                add_to_collection('/evolve/add_to_collection/', this.drawing.id, 'Public')
                    .then(data => {
                            console.log(data);
                            alert( this.drawing.id + ' saved to public');

                    });


            },
            private: function (event) {
                    add_to_collection('/evolve/add_to_collection/', this.drawing.id, 'Private')
                    .then(data => {
                            console.log(data);
                            alert( this.drawing.id + ' saved to private');

                    });
            },

            rating: function (rating) {
                console.log(this.current_rating);
                this.current_rating = rating ;
                add_rating('/evolve/add_rating/', this.drawing.id, rating)
                        .then(data => {
                            console.log(this.drawing.id, rating );
                            alert( this.drawing.id + ' saved to private');

                    });
            }
        }
});


var app = new Vue({
    delimiters: ['[[', ']]'],
    el: '#drawing-section',
    data: {
        drawings: [],
        sample_size:3
    }
});


async function add_rating(endpoint, individual_id, rating)
{
    const options = {
        method: 'POST',
        body: JSON.stringify({individual_id: individual_id, rating:rating}),
        headers: {
            "X-CSRFToken": getCookie('csrftoken'),
            'Content-Type': 'application/json'

        }
    }
    const res = await fetch(endpoint , options);
    let data = await res.json();

  return data.result;

}

function getCookie(name) {
  if (!document.cookie) {
    return null;
  }

  const xsrfCookies = document.cookie.split(';')
    .map(c => c.trim())
    .filter(c => c.startsWith(name + '='));

  if (xsrfCookies.length === 0) {
    return null;
  }

  return decodeURIComponent(xsrfCookies[0].split('=')[1]);
}


async function fetchCollections(endpoint) {
  const res = await fetch(endpoint);
  let data = await res.json();

  data = data.collections.map(collection => collection.name);
  return data;

}



async function getSample(endpoint, sample_size)
{
    const options = {
        method: 'POST',
        body: JSON.stringify({"jsonrpc": "2.0", "method": "get_sample", "params": [sample_size], "id": 1 }),
        headers: {
            "X-CSRFToken": getCookie('csrftoken'),
            'Content-Type': 'application/json'

        }
    }
    const res = await fetch(endpoint, options);
    let data = await res.json();

 // data = data.collections.map(collection => collection.name);
  return data.result;

}


async function add_to_collection(endpoint, individual_id, name)
{
    const options = {
        method: 'POST',
        body: JSON.stringify({individual_id: individual_id, visibility:name}),
        headers: {
            "X-CSRFToken": getCookie('csrftoken'),
            'Content-Type': 'application/json'

        }
    }
    const res = await fetch(endpoint , options);
    let data = await res.json();

  return data.result;

}


