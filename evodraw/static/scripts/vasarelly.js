
class Triangle
{

    constructor( x1, y1, x2, y2, x3, y3)
    {
        this.x1 = x1;
        this.y1 = y1;
        this.x2 = x2;
        this.y2 = y2;
        this.x3 = x3;
        this.y3 = y3;
    }
    display( f, sketch)
    {
        //stroke(1);
        sketch.noStroke();
        // int [] alpha = {0,127,192,192,225,255,255}  ;
        // int [] alpha = {0,0,0,0,0,255}  ;

        //  fill(f.hex, alpha[int(random(6) ) ]);
        //  fill(fill.hex, alpha[int(random(6) ) ]);
        sketch.fill(f);
        //fill(pallete[int(random(11))].hex);

        //smooth();
        sketch.triangle(this.x1, this.y1,this.x2, this.y2, this.x3, this.y3);

    }

}



var s = function (sketch) {
       var chromosome = [
        2,   2,   2,  2,  2,  2,
        2,   11,  11, 2, 2,  2,
        2,   2,   2,  2,  2,  2,
        2,   2,   0,  11, 2,  2,
        2,   2,   0,  11, 2,  2,
        2,   2,   2,  2,  2,  2,
        2,   2,   2,  2,  2,  2,
        2,   2,   2,  2,  2,  2,
        2,   2,   2,  2,  2,  2,
        2,   2,   2,  2,  2,  2,
        2,   2,   2,  2,  2,  2
        ];

       var pallete = [];

       var CANVAS_SIZE = 400;
       var ROWS = 5;

       var triangles =[];

       sketch.getChromosome = function() { return chromosome; }
       sketch.setChromosome = function(new_chromosome ) { chromosome = new_chromosome; }

       sketch.getPoints = function(){ return trian; }
       sketch.setup = function () {

           sketch.createCanvas(CANVAS_SIZE,CANVAS_SIZE);



    sketch.noLoop();


    sketch.append( pallete, sketch.color('#333333')); //Gris Oscuro
    sketch.append( pallete, sketch.color('#7B2B83')); //Purple
    sketch.append( pallete, sketch.color('#CCCCCC')); //Gris Claro
    sketch.append( pallete, sketch.color('#AEDD3C')); //Verde

    sketch.append( pallete, sketch.color('#00A7E5')); // Azul Cielo
    sketch.append( pallete, sketch.color('#E4D5ED')); // Purple Claro
    sketch.append( pallete, sketch.color('#777777')); // Gris Oscuro
    sketch.append( pallete, sketch.color('#A7005B')); // Rojo

    sketch.append( pallete, sketch.color('#000000')); //Gris Oscuro !!!
    sketch.append( pallete, sketch.color('#F89829')); // Naranjita
    sketch.append( pallete, sketch.color('#B31E6D')); // Rosa Claro
    sketch.append( pallete, sketch.color('#FFFFFF')); // Blanco !!!
    sketch.background(pallete[2]);

    //
    // Base y altura para hacer el grid
    //

    var lado = 48;
    var mitad = lado/2;
    var altura = sketch.int ( sketch.pow( sketch.pow( lado,2) - sketch.pow( lado/2,2), 0.5));
    var xorigen = (CANVAS_SIZE-(altura*6)) / 2;
    var yorigen = (CANVAS_SIZE-(altura*7)) / 2 + mitad;



    var c = 0;

    for (var j = 0; j<ROWS; j++ )
    {

        for (var i = 0; i<3;i++)
        {

            sketch.append( triangles, new Triangle(xorigen + (altura*2*i),           yorigen,
                xorigen + altura + (altura*2*i),  yorigen - mitad,
                xorigen + altura + (altura*2*i),  yorigen + mitad));

            sketch.append( triangles, new Triangle(xorigen + (altura*2*(i+1))     ,  yorigen,
                xorigen + altura + (altura*2*i), yorigen - mitad,
                xorigen + altura + (altura*2*i), yorigen +mitad));
        }

        for (var i = 0; i<3;i++)
        {
            sketch.append( triangles, new Triangle( xorigen + (altura*2*i),           yorigen,
                xorigen + altura + (altura*2*i),  yorigen + mitad,
                xorigen + (altura*2*i),           yorigen + lado
            ));

            sketch.append( triangles, new Triangle( xorigen + altura + (altura*2*(i)) ,  yorigen +mitad ,
                xorigen + (altura*2*(i+1))     ,  yorigen,
                xorigen + (altura*2*(i+1))     ,  yorigen + lado
            ));
        }

        yorigen += lado;
    }

    for (var i = 0; i<3;i++)
    {
        sketch.append( triangles, new Triangle( xorigen + (altura*2*i),           yorigen,
            xorigen + altura + (altura*2*i),  yorigen - mitad,
            xorigen + altura + (altura*2*i),  yorigen + mitad));


        sketch.append( triangles, new Triangle(xorigen + (altura*2*(i+1))     ,  yorigen,
            xorigen + altura + (altura*2*i), yorigen - mitad,
            xorigen + altura + (altura*2*i), yorigen +mitad));

    }

    }

    sketch.draw = function()
    {
        for (var j= 0; j< triangles.length; j++)
        {
            triangles[j].display(pallete[chromosome[j]], sketch);
        }

    }
    sketch.paint = function()
    {
        for (var j= 0; j< triangles.length; j++)
        {
        triangles[j].display(pallete[chromosome[j]], sketch);
        }

    }


}












