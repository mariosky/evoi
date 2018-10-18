


export class Triangle
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
    display( f)
    {
        //stroke(1);
        noStroke();
        // int [] alpha = {0,127,192,192,225,255,255}  ;
        // int [] alpha = {0,0,0,0,0,255}  ;

        //  fill(f.hex, alpha[int(random(6) ) ]);
        //  fill(fill.hex, alpha[int(random(6) ) ]);
        fill(f);
        //fill(pallete[int(random(11))].hex);

        //smooth();
        triangle(this.x1, this.y1,this.x2, this.y2, this.x3, this.y3);

    }

}


export class Vasarelly{

    constructor( ) {
        this.chromosome = [
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

        this.pallete = [];

        this.CANVAS_SIZE = 400;
        this.ROWS = 5;

        this.triangles =[]
  }

        getChromosome() { return chromosome; }
        getPoints() { return trian; }
        setup()
{
    var canvas = createCanvas(this.CANVAS_SIZE,this.CANVAS_SIZE);

    canvas.parent('sketch-holder');

    noLoop();


    append( this.pallete, color('#333333')); //Gris Oscuro
    append( this.pallete, color('#7B2B83')); //Purple
    append( this.pallete, color('#CCCCCC')); //Gris Claro
    append( this.pallete, color('#AEDD3C')); //Verde

    append( this.pallete, color('#00A7E5')); // Azul Cielo
    append( this.pallete, color('#E4D5ED')); // Purple Claro
    append( this.pallete, color('#777777')); // Gris Oscuro
    append( this.pallete, color('#A7005B')); // Rojo

    append( this.pallete, color('#000000')); //Gris Oscuro !!!
    append( this.pallete, color('#F89829')); // Naranjita
    append( this.pallete, color('#B31E6D')); // Rosa Claro
    append( this.pallete, color('#FFFFFF')); // Blanco !!!
    background(this.pallete[2]);

    //
    // Base y altura para hacer el grid
    //

    var lado = 32;
    var mitad = lado/2;
    var altura = int ( pow( pow( lado,2) - pow( lado/2,2), 0.5));
    var xorigen = (this.CANVAS_SIZE-(altura*6)) / 2;
    var yorigen = ((this.CANVAS_SIZE-(altura*7)) / 2 )+mitad;



    var c = 0;

    for (var j = 0; j<ROWS; j++ )
    {

        for (var i = 0; i<3;i++)
        {

            append( this.triangles, new Triangle(xorigen + (altura*2*i),           yorigen,
                xorigen + altura + (altura*2*i),  yorigen - mitad,
                xorigen + altura + (altura*2*i),  yorigen + mitad));

            append( this.triangles, new Triangle(xorigen + (altura*2*(i+1))     ,  yorigen,
                xorigen + altura + (altura*2*i), yorigen - mitad,
                xorigen + altura + (altura*2*i), yorigen +mitad));
        }

        for (var i = 0; i<3;i++)
        {
            append( this.triangles, new Triangle( xorigen + (altura*2*i),           yorigen,
                xorigen + altura + (altura*2*i),  yorigen + mitad,
                xorigen + (altura*2*i),           yorigen + lado
            ));

            append( this.triangles, new Triangle( xorigen + altura + (altura*2*(i)) ,  yorigen +mitad ,
                xorigen + (altura*2*(i+1))     ,  yorigen,
                xorigen + (altura*2*(i+1))     ,  yorigen + lado
            ));
        }

        yorigen += lado;
    }

    for (var i = 0; i<3;i++)
    {
        append( this.triangles, new Triangle( xorigen + (altura*2*i),           yorigen,
            xorigen + altura + (altura*2*i),  yorigen - mitad,
            xorigen + altura + (altura*2*i),  yorigen + mitad));


        append( this.triangles, new Triangle(xorigen + (altura*2*(i+1))     ,  yorigen,
            xorigen + altura + (altura*2*i), yorigen - mitad,
            xorigen + altura + (altura*2*i), yorigen +mitad));

    }

    }
draw()
{
    for (var j= 0; j< this.triangles.length; j++)
    {
        this.triangles[j].display(this.pallete[chromosome[j]]);
    }

}

paint()
{
    for (var j= 0; j< this.triangles.length; j++)
    {
        this.triangles[j].display(this.pallete[chromosome[j]]);
    }

}
}
