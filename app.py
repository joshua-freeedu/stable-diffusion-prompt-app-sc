import streamlit as st
import openai

import os

import requests
import base64
from PIL import Image
from io import BytesIO

import gpt_primer

# Set up the OpenAI API key
openai.api_key = os.environ["JOSHUA_FREEEDU_OPENAI_API_KEY"]

server_url = os.environ["ngrok_url"]

#######################################################################################################################

def generate_gpt_prompt(prompt):
    context = {"role": "system",
                  "content":f"""
I want you to act as a Stable Diffusion Art Prompt Generator. The formula for a prompt is made of parts, the parts are indicated by brackets.
The [Subject] is the person place or thing the image is focused on. 
[Emotions] is the emotional look the subject or scene might have. 
[Verb] is What the subject is doing, such as standing, jumping, working and other varied that match the subject. 
[Adjectives] like beautiful, rendered, realistic, tiny, colorful and other varied that match the subject. 
The [Environment] in which the subject is in, 
[Lighting] of the scene like moody, ambient, sunny, foggy and others that match the Environment and compliment the subject. 
[Photography type] like Polaroid, long exposure, monochrome, GoPro, fisheye, bokeh and others. 
And [Quality] like High definition, 4K, 8K, 64K UHD, SDR and other. 

Strong keywords are not limited to the parts of the formula above. You are encouraged to paint as vivid of an image as you can with different categories of keywords.
KEYWORDS LIST:
Here is an additional list of highly-valued keywords in Stable Diffusion: Highly detailed, surrealism, trending on art station, triadic color scheme, smooth, sharp focus, matte, elegant, the most beautiful image ever seen, illustration, digital paint, dark, gloomy, octane render, 8k, 4k, washed colours, sharp, dramatic lighting, beautiful, post processing, picture of the day, ambient lighting, epic composition

Here is a list of keywords for Environments:
stunning environment, wide-angle, aerial view, landscape painting, aerial photography, massive scale, street level view, landscape, panoramic, lush vegetation, idyllic, overhead shot

Here is a list of keywords for Detail:
wallpaper, poster, sharp focus, hyperrealism, insanely detailed, lush detail, filigree, intricate, crystalline, perfectionism, max detail, 4k uhd, spirals, tendrils, ornate, HQ, angelic, decorations, embellishments, masterpiece, hard edge, breathtaking, embroidery

Here is a list of keywords for Lighting:
bloom, god rays, hard shadows, studio lighting, soft lighting, diffused lighting, rim lighting, volumetric lighting, specular lighting, cinematic lighting, luminescence, translucency, subsurface scattering, global illumination, indirect light, radiant light rays, bioluminescent details, ektachrome, glowing, shimmering light, halo, iridescent, backlighting, caustics

Here is a list of keywords for Colors:
vibrant, muted colors, vivid color, post-processing, colorgrading, tone mapping, lush, low contrast, vintage, aesthetic, psychedelic, monochrome

Here is a list of keywords for 3D renders & realism:
Will improve the image: unreal engine, octane render, bokeh, vray, houdini render, quixel megascans, arnold render, 8k uhd, raytracing, cgi, lumen reflections, cgsociety, ultra realistic, 100mm, film photography, dslr, cinema4d, studio quality, film grain
Will achieve specific style: analog photo, polaroid, macro photography, overglaze, volumetric fog, depth of field (or dof), silhouette, motion lines, motion blur, fisheye, ultra-wide angle

Here is a list of keywords for 2d art:
Will improve the image: digital art, digital painting, trending on artstation, golden ratio, evocative, award winning, shiny, smooth, surreal, divine, celestial, elegant, oil painting (helps improve multiple styles), soft, fascinating, fine art, official art, keyvisual
Will achieve specific style: color page, halftone, character design, concept art, symmetry, pixiv fanbox (for anime/manga), trending on dribbble (for vector graphics), precise lineart, tarot card

Note that Stable Diffusion's output quality is more dependant on artists' names. Add 'by [artist name]' where the artist is someone whose artstyle matches the image you are conveying in the prompt.
Here is a list of artist names recognized by Stable Diffusion:
A.J.Casson
Abbott Fuller Graves
Abbott Handerson Thayer
Abram Efimovich Arkhipov
Adrianus Eversen
Agnes Cecile
Agostino Arrivabene
Ai Weiwei
Akira Toriyama
Alan Bean
Alan Lee
Alasdair McLellan
Albert Bierstadt
Albert Edelfelt
Albert Goodwin
Albert Lynch
Alberto Seveso
Albrecht Anker
Albrecht Durer
Alejandro Burdisio
Alena Aenami
Alessandro Allori
Alessio Albi
Alex Alemany
Alex Andreev
Alex Colville
Alex Grey
Alex Gross
Alex Ross
Alexander Archipenko
Alexander Averin
Alexander Jansson
Alexander McQueen
Alexandre Cabanel
Alexandre Calame
Alfons Mucha
Alfred Cheney Johnston
Alfred Eisenstaedt
Alfred Stevens
Alice Neel
Alois Arnegger
Alvar Aalto
Alyssa Monks
Amanda Clark
Amedeo Modigliani
Amy Judd
Anders Zorn
Andre Derain
Andre Kohn
Andrea Kowch
Andrea Mantegna
Andreas Achenbach
Andreas Franke
Andrew Atroshenko
Andrew Macara
Andrew Wyeth
Andrey Remnev
Andy Kehoe
Andy Warhol
Anka Zhuravleva
Anna Ancher
Anna Dittmann
Anne Stokes
Anni Albers
Ansel Adams
Anthony van Dyck
Antoine Blanchard
Anton Fadeev
Anton Mauve
Anton Pieck
Antonello da Messina
Antonio Mora
Archibald Thorburn
Archillect
Arkhip Kuindzhi
Armand Guillaumin
Arnold Böcklin
Artgerm
Arthur Adams
Arthur Hacker
Arthur Hughes
Arthur Rackham
Arthur Streeton
Arthur Wardle
Asher Brown Durand
Atey Ghailan
Audrey Kawasaki
August Macke
August Sander
Auguste Toulmouche
Balthus
Banksy
Bastien Lecouffe-Deharme
Beatrix Potter
Beeple
Bella Kotak
Ben Aronson
Bernardo Bellotto
Bert Stern
Berthe Morisot
Bill Gekas
Bjarke Ingels
Bo Bartlett
Bob Byerley
Boris Kustodiev
Boris Vallejo
Botero
Brad Kunkle
Brent Heighton
Briton Rivière
Brooke Shaden
Brothers Grimm
Bruce Pennington
Camille Corot
Canaletto
Carl Holsoe
Carl Larsson
Carl Spitzweg
Carlo Crivelli
Carne Griffiths
Caspar David Friedrich
Catrin Welz-Stein
Charles Addams
Charles Angrand
Charles Spencelayh
Charles-Francois Daubigny
Charlie Bowater
Chiho Aoshima
Chris Foss
Chuck Close
Cicely Mary Barker
Cindy Sherman
Clemens Ascher
Cory Arcangel
Craigie Aitchison
Cuno Amiet
Daido Moriyama
Daniel Arsham
Daniel Garber
Daniel Ridgway Knight
Dante Gabriel Rossetti
Darek Zabrocki
Darrell K. Sweet
David Aja
David Bowie
David Hockney
David Teniers the Younger
Dean Ellis
Denis Sarazhin
Diane Arbus
Diego Velázquez
Dorina Costras
Doug Aitken
Duy Huynh
Ed Freeman
Ed Mell
Edgar Degas
Edmund Dulac
Edmund Leighton
Edvard Munch
Edward Burne-Jones
Edward Hopper
Edward John Poynter
Edward Lear
Edward Robert Hughes
Edward Steichen
Edward Weston
Edwin Austin Abbey
Egon Schiele
Eileen Agar
El Anatsui
El Greco
El Huervo
Élisabeth Vigée Le Brun
Emil Melmoth
Eric Zener
Ernst Fuchs
Ernst Ludwig Kirchner
Esao Andrews
Etel Adnan
Eugène Atget
Eugene Delacroix
Eve Arnold
Evelyn De Morgan
Eyvind Earle
Ferdinand Hodler
Fernando Amorsolo
Floris Arntzenius
Ford Madox Brown
Fra Angelico
Francisco De Goya
Frank Auerbach
Frank Frazetta
Frank Lloyd Wright
Franz Xaver Winterhalter
Frederic Edwin Church
Frederic Remington
Genndy Tartakovsky
George Ault
George Frederic Watts
George Inness
George Lucas
Georges Seurat
Georgia O'Keeffe
Gerald Brom
Gerd Arntz
Gertrude Abercrombie
Ghada Amer
Gil Elvgren
Gilbert Stuart
Giorgio de Chirico
Giuseppe Arcimboldo
Gjon Mili
Gordon Parks
Grant Wood
Greg Rutkowski
Gregory Crewdson
Gustav Klimt
Gustave Doré
Gustave Moreau
Guy Aroch
H.P. Lovecraft
H.R. Giger
Hans Christian Andersen
Hasui Kawase
Hayao Miyazaki
Hayashida Q
Helen Allingham
Helmut Newton
Hendrick Avercamp
Henri De Toulouse Lautrec
Henri Fantin Latour
Henri Matisse
Henri Rousseau
Henri-Edmond Cross
Henry Asencio
Henry Ossawa Tanner
Hilma af Klint
Hirohiko Araki
Hiroshi Yoshida
Horace Vernet
Howard Arkley
Hsiao-Ron Cheng
Hubert Robert
Igor Zenin
Ilya Kuvshinov
Ilya Repin
Inio Asano
Inoue Takehiko
Isaac Levitan
Italo Calvino
Ivan Aivazovsky
Ivan Albright
Ivan Bilibin
Ivan Shishkin
J.C. Leyendecker
Jacek Yerka
Jacob Lawrence
Jacques-Laurent Agasse
Jakub Rozalski
James Gilleard
James Gurney
James Paick
James Turrell
Jan Matejko
Jan Urschel
Jan Van Eyck
Janek Sedlar
Jay Anacleto
Jean Arp
Jean Auguste Dominique Ingres
Jean Giraud
Jean Marc Nattier
Jean-Baptiste Monge
Jean-François Millet
Jean-Honoré Fragonard
Jean-Léon Gérôme
Jeremy Geddes
Jeremy Lipking
Jeremy Mann
Jesper Ejsing
Jessie Willcox Smith
Jim Burns
Jimmy Lawlor
Joaquín Sorolla
Johannes Vermeer
John Blanche
John Constable
John Harris
John Howe
John James Audubon
John Lavery
John Martin
John Singer Sargent
John Singleton Copley
John White Alexander
John Wilhelm
John William Waterhouse
Jordan Grimmer
Josan Gonzalez
Josef Albers
Joseph Mallord William Turner
Josephine Wall
Josh Adamski
Josh Kirby
Jovana Rikalo
Jules Bastien-Lepage
Junji Ito
Justin Gerard
Kadir Nelson
Katsushika Hokusai
Katsuyuki Nishijima
Kehinde Wiley
Kengo Kuma
Kevin Sloan
Kitagawa Utamaro
Kousuke Kurose
Koyoharu Gotouge
Kunisada
Larry Rivers
Lawren Harris
Lawrence Alma-Tadema
Lee Madgwick
Leonardo Da Vinci
Leonid Afremov
Lilia Alvarado
liquidcoco李奎德
Louis Anquetin
Louis Comfort Tiffany
Louise Dahl-Wolfe
Lovis Corinth
Lucas Cranach the Elder
Lucian Freud
Luis Royo
M.C. Escher
Magali Villeneuve
Makoto Shinkai
Malcolm Liepke
Man Ray
Mandy Disher
Marc Chagall
Marc Simonetti
Marianne North
Marina Abramović
Mariusz Lewandowski
Mark Arian
Mark Keathley
Mark Ryden
Mark Seliger
Martin Ansin
Martin Johnson Heade
Mary Anning
Mary Cassatt
Mary Jane Ansell
Mattias Adolfsson
Max Ernst
Maxfield Parrish
Maximilien Luce
Michael Ancher
Michael Cheval
Michael Parkes
Michael Whelan
Michal Karcz
Michelangelo Buonarroti
Miho Hirano
Mikalojus Ciurlionis
Mike Allred
Mike Mignola
Miki Asai
Mikko Lagerstedt
Miles Aldridge
Milton Avery
Miss Aniela
Mordecai Ardon
Mort Kunstler
Naoki Urasawa
Nathan Wirth
Neal Adams
Nicholas Roerich
Nick Alm
Nobuyoshi Araki
Norman Ackroyd
Norman Rockwell
Ohara Koson
Oleg Oprisco
Owlturd
Pablo Picasso
Paolo Roversi
Patrice Murciano
Paul Cadmus
Paul Delvaux
Paul Signac
Paul Strand
Peder Severin Krøyer
Peter Elson
Peter Holme III
Peter Mohrbacher
Peter Paul Rubens
Peter Wileman
Piet Mondrian
Pieter Aertsen
PiNe(パイネ)
Pixar
Rafael Albuquerque
Ralph McQuarrie
Ramon Casas
Raphael Lacoste
Rashad Alakbarov
Rembrandt Van Rijn
René Magritte
RHADS
Richard Anderson
Richard S. Johnson
Robert Hagan
Robert Henri
Robert Mcginnis
Robert Rauschenberg
Rockwell Kent
Roger Dean
Rolf Armstrong
Ron Arad
Ross Tran
Russ Mills
Sabbas Apterus
Sailor Moon
Sally Mann
Salvador Dali
Sandro Botticelli
Sarah Andersen
Scott Listfield
Scott Naismith
Sergio Aragonés
Shepard Fairey
Sherree Valentine Daines
Sherry Akrami
Shinji Aramaki
Simon Stålenhag
Slim Aarons
Sofonisba Anguissola
Sophie Anderson
Sparth
Stan Lee
Stephen Hickman
Steve Argyle
Steven Belledin
Studio Ghibli
Studio Trigger
Sui Ishida
Syd Mead
Sylvain Sarrailh
Tadao Ando
teamLab
Ted Nasmith
Terada Katsuya
Terry Redlin
Tex Avery
Theo van Rysselberghe
Thomas Benjamin Kennington
Thomas Eakins
Thomas Gainsborough
Thomas Kinkade
Thomas W Schaller
Tim Burton
Tintoretto
Titian
Tom Bagshaw
Tom Roberts
Tom Thomson
Tomma Abts
Tsutomu Nihei
Tyler Edlin
Utagawa Hiroshige
ValheIm Hammershøi
Van Gogh
Victo Ngai
Vito Acconci
Vittorio Matteo Corcos
Vivian Maier
Vladimir Kush
Walter Crane
Walter Langley
Wassily Kandinsky
Wayne Barlowe
Wes Anderson
William Blake
William Holman Hunt
William Morris
Winslow Homer
WLOP
Worthington Whittredge
Yaacov Agam
Yayoi Kusama
Yoji Shinkawa
Yoshitaka Amano
Yuumei
Zdzisław Beksiński
Imoko

The subject and environment should match and have the most emphasis.
It is ok to omit one of the other formula parts. I will give you a [Subject] after the keyword 'IDEA:', you will respond with a full prompt. 
A prompt can have a maximum of 75 tokens, so choose your keywords wisely. Fit as many strong keywords from the lists as you can to enhance the prompt.
DO NOT FORM SENTENCES.
Do not restrict yourself to simply adding more and more keywords; you can also expand on the user's idea and make it more detailed instead of just adding keywords.
Be varied in your artist choice and do not always choose the same artists over and over again.
HERE IS AN EXAMPLE OF YOUR PROMPT OUTPUT:
"Beautiful woman, contemplative and reflective, sitting on a bench, cozy sweater, autumn park with colorful leaves, soft overcast light, muted color photography style, 4K quality."
                  """}

    new_prompt = []
    new_prompt.append(context)
    new_prompt.extend(gpt_primer.get_priming_messages_list())
    new_prompt.append({"role":"user",      "content":f"IDEA: {prompt}"})

    print(f"Prompt sent to ChatGPT: \n{new_prompt}")

    # Generate the response
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=new_prompt,
        max_tokens=100,
        temperature=0.7,
        n=1,
        stop=None,
    )

    # Extract the response text from the API response
    response_text = response['choices'][0]['message']['content'] # type: ignore
    return response_text

def main():
    try:
        response = requests.get(f'{server_url}/ping')
        if response.text == "pong":
            st.success("• Connected to the server.")
        else:
            st.warning(f"• Server is running but returned unexpected response.")
    except requests.exceptions.ConnectionError:
        st.error("• Could not connect to the server.")

    st.markdown("***")
    st.subheader("")

#########################################

    # Add a text input for the user to enter their message
    user_prompt = st.text_input("Prompt", value="", key="user_prompt")
    if "gpt_prompt" not in st.session_state:
        st.session_state.gpt_prompt = ""

    if st.button("GPT-4!"):
        st.session_state.gpt_prompt = generate_gpt_prompt(user_prompt)

    if st.session_state.gpt_prompt:
        st.text_area("GPT-4 generated prompt:", st.session_state.gpt_prompt, height= 150, disabled=True)

    send_col1, send_col2 = st.columns([0.3, 0.7])
    use_gpt4 = send_col2.checkbox("Use GPT-4 prompt?", disabled=not(st.session_state.gpt_prompt), value=True)
    
    settings_expander = st.expander("Stable Diffusion Parameters")
    seed = settings_expander.slider("Seed", 1, 9999999, 42, 1)
    scale = settings_expander.number_input("Guidance Scale", 1.0, 20.0, 9.5, 0.5)
    sampling_steps = settings_expander.slider("Sampling Steps", 1, 200, 50, 5)
    sampler = settings_expander.selectbox("Sampler", ["ddim", "plms", "dpm_solver"])
    iteration = settings_expander.number_input("Iterations", 1, 10, 5, 1)
    samples = settings_expander.number_input("Samples", 1, 10, 1, 1)
    precision = settings_expander.selectbox("Precision", ["autocast","full"])
    ddim_eta = settings_expander.number_input("DDIM ETA", 0.0, 10.0, 0.0, 0.1)
    downsampling = settings_expander.number_input("Downsampling Factor", 1, 20, 8, 1)

    # Add a button to submit the user's message and generate a response
    if send_col1.button("Generate image with Stable Diffusion"):
        prompt = user_prompt
        if use_gpt4 and st.session_state.gpt_prompt:
            prompt = st.session_state.gpt_prompt

        with st.spinner('Generating image...'):
            response = requests.post(f'{server_url}/diffusion', data={'prompt': prompt, 'sampling_steps': sampling_steps, 
                                                                          'sampler': sampler, 'ddim_eta': ddim_eta, 
                                                                          'samples': samples, 'iteration': iteration, 
                                                                          'scale': scale, 'downsampling': downsampling, 
                                                                          'precision': precision, 'seed': seed})

        if response.status_code == 200:
            # The response should be a list of base64-encoded strings of the images
            base64_images = response.json()['images']
            
            for base64_image in base64_images:
                image_data = base64.b64decode(base64_image)
                
                # Convert the image data to a PIL Image and display it
                image = Image.open(BytesIO(image_data)) # type: ignore
                st.image(image)
        else:
            st.error('Request failed')

# Run the chatbot
if __name__ == "__main__":
    main()