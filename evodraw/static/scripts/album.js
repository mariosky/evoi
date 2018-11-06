
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


                    });


            },
            private: function (event) {
                    add_to_collection('/evolve/add_to_collection/', this.drawing.id, 'Private')
                    .then(data => {
                            console.log(data);

                    });
            },

            remove_from_album: function (event) {

                remove_from_my_album('/evolve/remove_from_my_album/', this.drawing.id)
                    .then(data => {
                        console.log(data);
                        alert( app.drawings.indexOf(this.drawing)+ ' removed');


                    });
            }


        }
});


var app = new Vue({
    delimiters: ['[[', ']]'],
    el: '#drawing-section',
    data: {
        drawings: [],

    },
    methods: {
        delete_drawing: function(index) {
            console.log( this.drawings[index].id );

            remove_from_my_album('/evolve/remove_from_my_album/', this.drawings[index].id)
                    .then(data => {
                        this.drawings.splice(index, 1);
                        console.log(data);
                        alert( app.drawings.indexOf(this.drawing)+ ' removed');


                    });



        }
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


async function remove_from_my_album(endpoint, individual_id)
{
    const options = {
        method: 'POST',
        headers: {
            "X-CSRFToken": getCookie('csrftoken'),
            'Content-Type': 'application/json'


        },
        body: JSON.stringify({individual_id:individual_id})

    }
    const res = await fetch(endpoint, options);
    let data = await res.json();

 // data = data.collections.map(collection => collection.name);
  return data;

}








