import os
import openai
import time
import os
from .files import read_file

def print_stream(string):
    for c in string:
        try:
            print(c, end="", flush=True)
            time.sleep(0.005)
        except KeyboardInterrupt:
            break


DEFAULT_SYSTEM_PROMPT = read_file("prompts/default_system_prompt.txt")
JSON_CORRECTOR_PROMPT = read_file("prompts/json_corrector_prompt.txt")
DICE_ROLL_PROMPT = read_file("prompts/dice_roll_prompt.txt")


class GPTModel:
  
    def __init__(self, model="gpt-3.5-turbo", system_prompt=DEFAULT_SYSTEM_PROMPT+DICE_ROLL_PROMPT, temperature=0.5):
        self.model = model
        self.conversation = [{"role": "system", "content": ""}]
        self.max_characters = 15000
        self.set_system_prompt(system_prompt)
        self.settings = {}
        self.api_url = "https://api.openai.com/v1/chat/completions"
        self.api_key = os.environ.get("OPENAI_API_KEY")
        self.stream = False
        self.stream_callback = lambda text: print_stream(text)
        self.functions = []
        self.temperature = temperature

    def get_system_prompt(self):
        return self.conversation[0]["content"]

    def set_system_prompt(self, new):
        if len(new) <= self.max_characters:
            self.conversation[0]["content"] = new
        else:
            print("Error: ", "system prompt too long")

    def reply_as_user(self, reply):
        if self.conversation[-1]["role"] in ["system", "assistant"]:
            self.conversation.append({"role": "user", "content": reply})
            return reply
        else:
            print("Error: ", "The user has already replied")
            return "Error: The user has already replied"
    
    def force_reply_as_user(self, reply):
        self.conversation.append({"role": "user", "content": reply})
        return reply

    def reply_as_assistant(self, reply):
        if self.conversation[-1]["role"] == "user":
            self.conversation.append({"role": "assistant", "content": reply})
            return reply

        else:
            print("Error: ", "The assistant has already replied")
            return "Error: The assistant has already replied"

    def force_reply_as_assistant(self, reply):
        self.conversation.append({"role": "assistant", "content": reply})
        return reply
        
    def generate(self):
        try:
            if len(self.functions) > 0:
                response = openai.ChatCompletion.create(
                    model = self.model,
                    messages = self.conversation,
                    temperature = self.temperature,
                    stream = self.stream,  # this time, we set stream=True,
                    functions = self.functions
                )
            else:
                response = openai.ChatCompletion.create(
                    model = self.model,
                    messages = self.conversation,
                    temperature = self.temperature,
                    stream = self.stream,  # this time, we set stream=True,
                )

            assistant_response = ""
            if self.stream:
                for chunk in response:
                    #print(chunk)
                    try:
                        char = chunk['choices'][0]['delta']['content']
                        #print(char, end="")
                        self.conversation[-1]['content'] += char
                        self.stream_callback(char)
                        assistant_response += char
                    except:
                        pass
            else:

                assistant_response = response['choices'][0]['message']
                if assistant_response.get('function_call'):
                    return assistant_response['function_call']
                else:
                    return assistant_response['content']
                

            return assistant_response

        except Exception as error:
            print("Error: ", error)
            return "Error generating response."
        
    def generate_assistant_reply(self, message=False, append=True):
        if message:
            self.reply_as_user(message)

        reply = self.generate()
        if not append:
            return reply
        
        if reply:
            self.reply_as_assistant(str(reply))

        self.prune()
        return reply
    
    def delete_last_message(self):
        self.conversation = self.conversation[:-1]

    def reset(self):
        self.conversation = self.conversation[:1]

    def character_count(self):
        return sum([len(c["content"]) for c in self.conversation])
    
    def prune(self):
        while self.character_count() > self.max_characters:
            del self.conversation[1]
            del self.conversation[1]

    def dump(self):
        return str(self.conversation)
    
    def pretty_dump(self):
        return '\n\n'.join([f'{message["role"]}: {message["content"]}' for message in self.conversation])

model = GPTModel(model="gpt-4")

model.set_system_prompt("You are an AI asssitant.")
print(model.generate_assistant_reply('''
Main menu

WikipediaThe Free Encyclopedia
Search Wikipedia
Search
Create account
Log in

Personal tools
WIKI loves monuments		Photograph a monument,
help Wikipedia and win!Hide
Contents hide
(Top)
Etymology
History
Toggle History subsection
Geography
Toggle Geography subsection
Politics
Toggle Politics subsection
Economy
Toggle Economy subsection
Demographics
Toggle Demographics subsection
Culture
Toggle Culture subsection
See also
Notes
References
External links
Germany

Article
Talk
Read
View source
View history

Tools
Coordinates: 51°N 9°E
Featured article
Page semi-protected
Listen to this article
From Wikipedia, the free encyclopedia
(Redirected from Deutchland)
"Deutschland" redirects here. For other uses, see Deutschland (disambiguation) and Germany (disambiguation).
"Federal Republic of Germany" redirects here. For the republic from 1949 to 1990, see West Germany. For the republic since 1990, see History of Germany (1990–present).
Federal Republic of Germany
Bundesrepublik Deutschland (German)
Flag of Germany
Flag
Coat of arms of Germany
Coat of arms
Anthem: "Deutschlandlied"[a]
("Song of Germany")
1:15

Show globe
Show map of Europe
Show all
Location of Germany (dark green)
 in Europe (light green & dark grey)
 in the European Union (light green)

Capital
and largest city
Berlin[b]
52°31N 13°23E
Official languages	German[c]
Demonym(s)	German
Government	Federal parliamentary republic[4]
• President
Frank-Walter Steinmeier
• Chancellor
Olaf Scholz
Legislature	Bundestag, Bundesrat[d]
Area
• Total
357,600 km2 (138,100 sq mi)[5] (63rd)
• Water (%)
1.27 (2015)[6]
Population
• Q1 2023 estimate
Neutral increase 84,432,670[7] (19th)
• Density
232/km2 (600.9/sq mi) (58th)
GDP (PPP)	2023 estimate
• Total
Increase $5.546 trillion[8] (5th)
• Per capita
Increase $66,132[8] (18th)
GDP (nominal)	2023 estimate
• Total
Increase $4.309 trillion[8] (4th)
• Per capita
Increase $51,384[8] (20th)
Gini (2020)	Negative increase 30.5[9]
medium
HDI (2021)	Increase 0.942[10]
very high · 9th
Currency	Euro (€) (EUR)
Time zone	UTC+1 (CET)
• Summer (DST)
UTC+2 (CEST)
Driving side	right
Calling code	+49
ISO 3166 code	DE
Internet TLD	.de
Germany,[e] officially the Federal Republic of Germany (German: Bundesrepublik Deutschland),[f] is a country in the western region of Central Europe. It is the second-most populous country in Europe after Russia, and the most populous member state of the European Union. Germany is situated between the Baltic and North seas to the north, and the Alps to the south. Its 16 constituent states are bordered by Denmark to the north, Poland and the Czech Republic to the east, Austria and Switzerland to the south, and France, Luxembourg, Belgium, and the Netherlands to the west. The nation's capital and most populous city is Berlin and its main financial centre is Frankfurt; the largest urban area is the Ruhr.

Various Germanic tribes have inhabited the northern parts of modern Germany since classical antiquity. A region named Germania was documented before AD 100. In 962, the Kingdom of Germany formed the bulk of the Holy Roman Empire. During the 16th century, northern German regions became the centre of the Protestant Reformation. Following the Napoleonic Wars and the dissolution of the Holy Roman Empire in 1806, the German Confederation was formed in 1815.

Formal unification of Germany into the modern nation-state was commenced on 18 August 1866 with the North German Confederation Treaty establishing the Prussia-led North German Confederation later transformed in 1871 into the German Empire. After World War I and the German Revolution of 1918–1919, the Empire was in turn transformed into the semi-presidential Weimar Republic. The Nazi seizure of power in 1933 led to the establishment of a totalitarian dictatorship, World War II, and the Holocaust. After the end of World War II in Europe and a period of Allied occupation, in 1949, Germany as a whole was organized into two separate polities with limited sovereignty: the Federal Republic of Germany, generally known as West Germany, and the German Democratic Republic, known as East Germany, while Berlin continued its de jure Four Power status. The Federal Republic of Germany was a founding member of the European Economic Community and the European Union, while the German Democratic Republic was a communist Eastern Bloc state and member of the Warsaw Pact. After the fall of communist led-government in East Germany, German reunification saw the former East German states join the Federal Republic of Germany on 3 October 1990.

Germany has been described as a great power with a strong economy; it has the largest economy in Europe, the world's fourth-largest economy by nominal GDP and the fifth-largest by PPP. As a global power in industrial, scientific and technological sectors, it is both the world's third-largest exporter and importer. As a developed country it offers social security, a universal health care system and a tuition-free university education. Germany is a member of the United Nations, European Union, NATO, Council of Europe, G7, G20 and OECD. It has the third-greatest number of UNESCO World Heritage Sites.

Etymology
Further information: Names of Germany, Germani, and Germania
The English word Germany derives from the Latin Germania, which came into use after Julius Caesar adopted it for the peoples east of the Rhine.[12] The German term Deutschland, originally diutisciu land ('the German lands') is derived from deutsch (cf. Dutch), descended from Old High German diutisc 'of the people' (from diot or diota 'people'), originally used to distinguish the language of the common people from Latin and its Romance descendants. This in turn descends from Proto-Germanic *þiudiskaz 'of the people' (see also the Latinised form Theodiscus), derived from *þeudō, descended from Proto-Indo-European *tewtéh₂- 'people', from which the word Teutons also originates.[13]

History
Main article: History of Germany
For a chronological guide, see Timeline of German history.
Pre-human ancestors, the Danuvius guggenmosi, who were present in Germany over 11 million years ago, are theorized to be among the earliest ones to walk on two legs.[14] Ancient humans were present in Germany at least 600,000 years ago.[15] The first non-modern human fossil (the Neanderthal) was discovered in the Neander Valley.[16] Similarly dated evidence of modern humans has been found in the Swabian Jura, including 42,000-year-old flutes which are the oldest musical instruments ever found,[17] the 40,000-year-old Lion Man,[18] and the 35,000-year-old Venus of Hohle Fels.[19] The Nebra sky disk, created during the European Bronze Age, has been attributed to a German site.[20]

Germanic tribes and the Frankish Empire
Main articles: Jastorf culture, Germanic peoples, Germania, Migration Period, and Frankish Realm

A model of Augusta Treverorum, part of the Roman Empire in the 4th century
The Germanic peoples are thought to date from the Nordic Bronze Age, early Iron Age, or the Jastorf culture.[21][22] From southern Scandinavia and northern Germany, they expanded south, east, and west, coming into contact with the Celtic, Iranian, Baltic, and Slavic tribes.[23]

Under Augustus, the Roman Empire began to invade lands inhabited by the Germanic tribes, creating a short-lived Roman province of Germania between the Rhine and Elbe rivers. In 9 AD, three Roman legions were defeated by Arminius in the Battle of the Teutoburg Forest.[24] The outcome of this battle dissuaded the Romans from their ambition of conquering Germania, and is thus considered one of the most important events in European history.[25] By 100 AD, when Tacitus wrote Germania, Germanic tribes had settled along the Rhine and the Danube (the Limes Germanicus), occupying most of modern Germany. However, Baden-Württemberg, southern Bavaria, southern Hesse and the western Rhineland had been incorporated into Roman provinces.[26][27][28]

Around 260, Germanic peoples broke into Roman-controlled lands.[29] After the invasion of the Huns in 375, and with the decline of Rome from 395, Germanic tribes moved farther southwest: the Franks established the Frankish Kingdom and pushed east to subjugate Saxony and Bavaria, and areas of what is today eastern Germany were inhabited by Western Slavic tribes.[26]

East Francia and the Holy Roman Empire
Main articles: East Francia and Holy Roman Empire

East Francia in 843

Martin Luther, born in Eisleben in 1483, challenged the indulgences of the Catholic Church, giving rise to the Reformation and Protestantism.
Charlemagne founded the Carolingian Empire in 800; it was divided in 843.[30] The eastern successor kingdom of East Francia stretched from the Rhine in the west to the Elbe river in the east and from the North Sea to the Alps.[30] Subsequently, the Holy Roman Empire emerged from it. The Ottonian rulers (919–1024) consolidated several major duchies.[31] In 996, Gregory V became the first German Pope, appointed by his cousin Otto III, whom he shortly after crowned Holy Roman Emperor. The Holy Roman Empire absorbed northern Italy and Burgundy under the Salian emperors (1024–1125), although the emperors lost power through the Investiture Controversy.[32]

Under the Hohenstaufen emperors (1138–1254), German princes encouraged German settlement to the south and east (Ostsiedlung).[33] Members of the Hanseatic League, mostly north German towns, prospered in the expansion of trade.[34] The population declined starting with the Great Famine in 1315, followed by the Black Death of 1348–1350.[35] The Golden Bull issued in 1356 provided the constitutional structure of the Empire and codified the election of the emperor by seven prince-electors.[36]

Johannes Gutenberg introduced moveable-type printing to Europe, laying the basis for the democratization of knowledge.[37] In 1517, Martin Luther incited the Protestant Reformation and his translation of the Bible began the standardization of the language; the 1555 Peace of Augsburg tolerated the "Evangelical" faith (Lutheranism), but also decreed that the faith of the prince was to be the faith of his subjects (cuius regio, eius religio).[38] From the Cologne War through the Thirty Years' Wars (1618–1648), religious conflict devastated German lands and significantly reduced the population.[39][40]

The Peace of Westphalia ended religious warfare among the Imperial Estates;[39] their mostly German-speaking rulers were able to choose Catholicism, Lutheranism, or Calvinism as their official religion.[41] The legal system initiated by a series of Imperial Reforms (approximately 1495–1555) provided for considerable local autonomy and a stronger Imperial Diet.[42] The House of Habsburg held the imperial crown from 1438 until the death of Charles VI in 1740. Following the War of the Austrian Succession and the Treaty of Aix-la-Chapelle, Charles VI's daughter Maria Theresa ruled as empress consort when her husband, Francis I, became emperor.[43][44]

From 1740, dualism between the Austrian Habsburg monarchy and the Kingdom of Prussia dominated German history. In 1772, 1793, and 1795, Prussia and Austria, along with the Russian Empire, agreed to the Partitions of Poland.[45][46] During the period of the French Revolutionary Wars, the Napoleonic era and the subsequent final meeting of the Imperial Diet, most of the Free Imperial Cities were annexed by dynastic territories; the ecclesiastical territories were secularised and annexed. In 1806 the Imperium was dissolved; France, Russia, Prussia, and the Habsburgs (Austria) competed for hegemony in the German states during the Napoleonic Wars.[47]

German Confederation and Empire
Main articles: German question, German Confederation, Unification of Germany, German Empire, and German colonial empire

The German Confederation in 1815
Following the fall of Napoleon, the Congress of Vienna founded the German Confederation, a loose league of 39 sovereign states. The appointment of the emperor of Austria as the permanent president reflected the Congress's rejection of Prussia's rising influence. Disagreement within restoration politics partly led to the rise of liberal movements, followed by new measures of repression by Austrian statesman Klemens von Metternich.[48][49] The Zollverein, a tariff union, furthered economic unity.[50] In light of revolutionary movements in Europe, intellectuals and commoners started the revolutions of 1848 in the German states, raising the German question. King Frederick William IV of Prussia was offered the title of emperor, but with a loss of power; he rejected the crown and the proposed constitution, a temporary setback for the movement.[51]

King William I appointed Otto von Bismarck as the minister president of Prussia in 1862. Bismarck successfully concluded the war with Denmark in 1864; the subsequent decisive Prussian victory in the Austro-Prussian War of 1866 enabled him to create the North German Confederation which excluded Austria. After the defeat of France in the Franco-Prussian War, the German princes proclaimed the founding of the German Empire in 1871. Prussia was the dominant constituent state of the new empire; the King of Prussia ruled as its Kaiser, and Berlin became its capital.[52][53]

In the Gründerzeit period following the unification of Germany, Bismarck's foreign policy as chancellor of Germany secured Germany's position as a great nation by forging alliances and avoiding war.[53] However, under Wilhelm II, Germany took an imperialistic course, leading to friction with neighbouring countries.[54] A dual alliance was created with the multinational realm of Austria-Hungary; the Triple Alliance of 1882 included Italy. Britain, France and Russia also concluded alliances to protect against Habsburg interference with Russian interests in the Balkans or German interference against France.[55] At the Berlin Conference in 1884, Germany claimed several colonies including German East Africa, German South West Africa, Togoland, and Kamerun.[56] Later, Germany further expanded its colonial empire to include holdings in the Pacific and China.[57] The colonial government in South West Africa (present-day Namibia), from 1904 to 1907, carried out the annihilation of the local Herero and Namaqua peoples as punishment for an uprising;[58][59] this was the 20th century's first genocide.[59]

The assassination of Austria's crown prince on 28 June 1914 provided the pretext for Austria-Hungary to attack Serbia and trigger World War I. After four years of warfare, in which approximately two million German soldiers were killed,[60] a general armistice ended the fighting. In the German Revolution (November 1918), Emperor Wilhelm II and the ruling princes abdicated their positions, and Germany was declared a federal republic. Germany's new leadership signed the Treaty of Versailles in 1919, accepting defeat by the Allies. Germans perceived the treaty as humiliating, which was seen by historians as influential in the rise of Adolf Hitler.[61] Germany lost around 13% of its European territory and ceded all of its colonial possessions in Africa and the Pacific.[62]

Weimar Republic and Nazi Germany
Main articles: Weimar Republic and Nazi Germany

Adolf Hitler, dictator of Nazi Germany from 1933 to 1945

A map of German-occupied Europe in 1942 during World War II with areas controlled by the German Reich shown in bold black
On 11 August 1919, President Friedrich Ebert signed the democratic Weimar Constitution.[63] In the subsequent struggle for power, communists seized power in Bavaria, but conservative elements elsewhere attempted to overthrow the Republic in the Kapp Putsch. Street fighting in the major industrial centres, the occupation of the Ruhr by Belgian and French troops, and a period of hyperinflation followed. A debt restructuring plan and the creation of a new currency in 1924 ushered in the Golden Twenties, an era of artistic innovation and liberal cultural life.[64][65][66]

The worldwide Great Depression hit Germany in 1929. Chancellor Heinrich Brüning's government pursued a policy of fiscal austerity and deflation which caused unemployment of nearly 30% by 1932.[67] The Nazi Party led by Adolf Hitler became the largest party in the Reichstag after a special election in 1932 and Hindenburg appointed Hitler as chancellor of Germany on 30 January 1933.[68] After the Reichstag fire, a decree abrogated basic civil rights and the first Nazi concentration camp opened.[69][70] On 23 March 1933, the Enabling Act gave Hitler unrestricted legislative power, overriding the constitution,[71] and marked the beginning of Nazi Germany. His government established a centralised totalitarian state, withdrew from the League of Nations, and dramatically increased the country's rearmament.[72] A government-sponsored programme for economic renewal focused on public works, the most famous of which was the Autobahn.[73]

In 1935, the regime withdrew from the Treaty of Versailles and introduced the Nuremberg Laws which targeted Jews and other minorities.[74] Germany also reacquired control of the Saarland in 1935,[75] remilitarised the Rhineland in 1936, annexed Austria in 1938, annexed the Sudetenland in 1938 with the Munich Agreement, and in violation of the agreement occupied Czechoslovakia in March 1939.[76] Kristallnacht (Night of Broken Glass) saw the burning of synagogues, the destruction of Jewish businesses, and mass arrests of Jewish people.[77]

In August 1939, Hitler's government negotiated the MolotovRibbentrop Pact that divided Eastern Europe into German and Soviet spheres of influence.[78] On 1 September 1939, Germany invaded Poland, beginning World War II in Europe;[79] Britain and France declared war on Germany on 3 September.[80] In the spring of 1940, Germany conquered Denmark and Norway, the Netherlands, Belgium, Luxembourg, and France, forcing the French government to sign an armistice. The British repelled German air attacks in the Battle of Britain in the same year. In 1941, German troops invaded Yugoslavia, Greece and the Soviet Union. By 1942, Germany and its allies controlled most of continental Europe and North Africa, but following the Soviet victory at the Battle of Stalingrad, the Allied reconquest of North Africa and invasion of Italy in 1943, German forces suffered repeated military defeats. In 1944, the Soviets pushed into Eastern Europe; the Western allies landed in France and entered Germany despite a final German counteroffensive. Following Hitler's suicide during the Battle of Berlin, Germany signed the surrender document on 8 May 1945, ending World War II in Europe[79][81] and Nazi Germany. Following the end of the war, surviving Nazi officials were tried for war crimes at the Nuremberg trials.[82][83]

In what later became known as the Holocaust, the German government persecuted minorities, including interning them in concentration and death camps across Europe. In total 17 million people were systematically murdered, including 6 million Jews, at least 130,000 Romani, 275,000 disabled people, thousands of Jehovah's Witnesses, thousands of homosexuals, and hundreds of thousands of political and religious opponents.[84] Nazi policies in German-occupied countries resulted in the deaths of an estimated 2.7 million Poles,[85] 1.3 million Ukrainians, 1 million Belarusians and 3.5 million Soviet prisoners of war.[86][82] German military casualties have been estimated at 5.3 million,[87] and around 900,000 German civilians died.[88] Around 12 million ethnic Germans were expelled from across Eastern Europe, and Germany lost roughly one-quarter of its pre-war territory.[89]

East and West Germany
Main articles: History of Germany (1945–1990), Allied-occupied Germany, West Germany, and East Germany

A map of Germany in 1947, following the end of World War II, including American, Soviet, British, and French occupation zones and the French-controlled Saarland. Territories east of the Oder-Neisse line were transferred to Poland and the Soviet Union under the terms of the Potsdam Conference.[90]
After Nazi Germany surrendered, the Allies partitioned Berlin and Germany's remaining territory into four occupation zones. The western sectors, controlled by France, the United Kingdom, and the United States, were merged on 23 May 1949 to form the Federal Republic of Germany (German: Bundesrepublik Deutschland); on 7 October 1949, the Soviet Zone became the German Democratic Republic (GDR) (German: Deutsche Demokratische Republik; DDR). They were informally known as West Germany and East Germany.[91] East Germany selected East Berlin as its capital, while West Germany chose Bonn as a provisional capital, to emphasise its stance that the two-state solution was temporary.[92]

West Germany was established as a federal parliamentary republic with a "social market economy". Starting in 1948 West Germany became a major recipient of reconstruction aid under the American Marshall Plan.[93] Konrad Adenauer was elected the first federal chancellor of Germany in 1949. The country enjoyed prolonged economic growth (Wirtschaftswunder) beginning in the early 1950s.[94] West Germany joined NATO in 1955 and was a founding member of the European Economic Community.[95] On 1 January 1957, the Saarland joined West Germany.[96]

East Germany was an Eastern Bloc state under political and military control by the Soviet Union via occupation forces and the Warsaw Pact. Although East Germany claimed to be a democracy, political power was exercised solely by leading members (Politbüro) of the communist-controlled Socialist Unity Party of Germany, supported by the Stasi, an immense secret service.[97] While East German propaganda was based on the benefits of the GDR's social programmes and the alleged threat of a West German invasion, many of its citizens looked to the West for freedom and prosperity.[98] The Berlin Wall, built in 1961, prevented East German citizens from escaping to West Germany, becoming a symbol of the Cold War.[99]

Tensions between East and West Germany were reduced in the late 1960s by Chancellor Willy Brandt's Ostpolitik.[100] In 1989, Hungary decided to dismantle the Iron Curtain and open its border with Austria, causing the emigration of thousands of East Germans to West Germany via Hungary and Austria. This had devastating effects on the GDR, where regular mass demonstrations received increasing support. In an effort to help retain East Germany as a state, the East German authorities eased border restrictions, but this actually led to an acceleration of the Wende reform process culminating in the Two Plus Four Treaty under which Germany regained full sovereignty. This permitted German reunification on 3 October 1990, with the accession of the five re-established states of the former GDR.[101] The fall of the Wall in 1989 became a symbol of the Fall of Communism, the Dissolution of the Soviet Union, German reunification and Die Wende.[102]

Reunified Germany and the European Union
Main articles: German reunification and History of Germany since 1990

The Berlin Wall during its fall in 1989 and the Brandenburg Gate (background) was one of the first developments in the end of the Cold War, leading ultimately to the dissolution of the Soviet Union.
United Germany was considered the enlarged continuation of West Germany so it retained its memberships in international organisations.[103] Based on the Berlin/Bonn Act (1994), Berlin again became the capital of Germany, while Bonn obtained the unique status of a Bundesstadt (federal city) retaining some federal ministries.[104] The relocation of the government was completed in 1999, and modernisation of the East German economy was scheduled to last until 2019.[105][106]

Since reunification, Germany has taken a more active role in the European Union, signing the Maastricht Treaty in 1992 and the Lisbon Treaty in 2007,[107] and co-founding the Eurozone.[108] Germany sent a peacekeeping force to secure stability in the Balkans and sent German troops to Afghanistan as part of a NATO effort to provide security in that country after the ousting of the Taliban.[109][110]

In the 2005 elections, Angela Merkel became the first female chancellor. In 2009, the German government approved a €50 billion stimulus plan.[111] Among the major German political projects of the early 21st century are the advancement of European integration, the energy transition (Energiewende) for a sustainable energy supply, the debt brake for balanced budgets, measures to increase the fertility rate (pronatalism), and high-tech strategies for the transition of the German economy, summarised as Industry 4.0.[112] During the 2015 European migrant crisis, the country took in over a million refugees and migrants.[113]

Geography
Main article: Geography of Germany

A physical map of Germany
Germany is the seventh-largest country in Europe;[4] bordering Denmark to the north, Poland and the Czech Republic to the east, Austria to the southeast, and Switzerland to the south-southwest. France, Luxembourg and Belgium are situated to the west, with the Netherlands to the northwest. Germany is also bordered by the North Sea and, at the north-northeast, by the Baltic Sea. German territory covers 357,022 km2 (137,847 sq mi), consisting of 348,672 km2 (134,623 sq mi) of land and 8,350 km2 (3,224 sq mi) of water.

Elevation ranges from the mountains of the Alps (highest point: the Zugspitze at 2,963 metres or 9,721 feet) in the south to the shores of the North Sea (Nordsee) in the northwest and the Baltic Sea (Ostsee) in the northeast. The forested uplands of central Germany and the lowlands of northern Germany (lowest point: in the municipality Neuendorf-Sachsenbande, Wilstermarsch at 3.54 metres or 11.6 feet below sea level[114]) are traversed by such major rivers as the Rhine, Danube and Elbe. Significant natural resources include iron ore, coal, potash, timber, lignite, uranium, copper, natural gas, salt, and nickel.[4]

Climate
Most of Germany has a temperate climate, ranging from oceanic in the north and west to continental in the east and southeast. Winters range from the cold in the Southern Alps to cool and are generally overcast with limited precipitation, while summers can vary from hot and dry to cool and rainy. The northern regions have prevailing westerly winds that bring in moist air from the North Sea, moderating the temperature and increasing precipitation. Conversely, the southeast regions have more extreme temperatures.[115]

From February 2019  2020, average monthly temperatures in Germany ranged from a low of 3.3 °C (37.9 °F) in January 2020 to a high of 19.8 °C (67.6 °F) in June 2019.[116] Average monthly precipitation ranged from 30 litres per square metre in February and April 2019 to 125 litres per square metre in February 2020.[117] Average monthly hours of sunshine ranged from 45 in November 2019 to 300 in June 2019.[118]

Biodiversity

Berchtesgaden National Park in Bavaria
The territory of Germany can be divided into five terrestrial ecoregions: Atlantic mixed forests, Baltic mixed forests, Central European mixed forests, Western European broadleaf forests, and Alps conifer and mixed forests.[119] As of 2016 51% of Germany's land area is devoted to agriculture, while 30% is forested and 14% is covered by settlements or infrastructure.[120]

Plants and animals include those generally common to Central Europe. According to the National Forest Inventory, beeches, oaks, and other deciduous trees constitute just over 40% of the forests; roughly 60% are conifers, particularly spruce and pine.[121] There are many species of ferns, flowers, fungi, and mosses. Wild animals include roe deer, wild boar, mouflon (a subspecies of wild sheep), fox, badger, hare, and small numbers of the Eurasian beaver.[122] The blue cornflower was once a German national symbol.[123]

The 16 national parks in Germany include the Jasmund National Park, the Vorpommern Lagoon Area National Park, the Müritz National Park, the Wadden Sea National Parks, the Harz National Park, the Hainich National Park, the Black Forest National Park, the Saxon Switzerland National Park, the Bavarian Forest National Park and the Berchtesgaden National Park.[124] In addition, there are 17 Biosphere Reserves,[125] and 105 nature parks.[126] More than 400 zoos and animal parks operate in Germany.[127] The Berlin Zoo, which opened in 1844, is the oldest in Germany, and claims the most comprehensive collection of species in the world.[128]

Politics
Main articles: Politics of Germany, Taxation in Germany, and Federal budget of Germany
	
Frank-Walter Steinmeier
President
(representative head of state)	Olaf Scholz
Chancellor
(head of government)
Germany is a federal, parliamentary, representative democratic republic. Federal legislative power is vested in the parliament consisting of the Bundestag (Federal Diet) and Bundesrat (Federal Council), which together form the legislative body. The Bundestag is elected through direct elections using the mixed-member proportional representation system. The members of the Bundesrat represent and are appointed by the governments of the sixteen federated states.[4] The German political system operates under a framework laid out in the 1949 constitution known as the Grundgesetz (Basic Law). Amendments generally require a two-thirds majority of both the Bundestag and the Bundesrat; the fundamental principles of the constitution, as expressed in the articles guaranteeing human dignity, the separation of powers, the federal structure, and the rule of law, are valid in perpetuity.[129]

The president, currently Frank-Walter Steinmeier, is the head of state and invested primarily with representative responsibilities and powers. He is elected by the Bundesversammlung (federal convention), an institution consisting of the members of the Bundestag and an equal number of state delegates.[4] The second-highest official in the German order of precedence is the Bundestagspräsident (President of the Bundestag), who is elected by the Bundestag and responsible for overseeing the daily sessions of the body.[130] The third-highest official and the head of government is the chancellor, who is appointed by the Bundespräsident after being elected by the party or coalition with the most seats in the Bundestag.[4] The chancellor, currently Olaf Scholz, is the head of government and exercises executive power through his Cabinet.[4]

Since 1949, the party system has been dominated by the Christian Democratic Union and the Social Democratic Party of Germany. So far every chancellor has been a member of one of these parties. However, the smaller liberal Free Democratic Party and the Alliance 90/The Greens have also been junior partners in coalition governments. Since 2007, the democratic socialist party The Left has been a staple in the German Bundestag, though they have never been part of the federal government. In the 2017 German federal election, the right-wing populist Alternative for Germany gained enough votes to attain representation in the parliament for the first time.[131][132]

Constituent states
Main articles: States of Germany, Federalism in Germany, and List of current Minister-presidents of the German federal states
Germany is a federation and.

Please confirm this information by saying "I confirm." Please say nothing else


'''))