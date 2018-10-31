
Vue.component('evo-drawing', {
  props: ['drawing'],
  template:"#evodrawing-template",
  delimiters: ['[[', ']]'],
  computed: {


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

    }
});




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



async function getAlbum(endpoint)
{
    const options = {
        method: 'GET',
        headers: {
            //"X-CSRFToken": getCookie('csrftoken'),
            'Content-Type': 'application/json'

        }
    }
    const res = await fetch(endpoint, options);
    let data = await res.json();

 // data = data.collections.map(collection => collection.name);
  return data;

}



