from matplotlib import pyplot as plt
import matplotlib
import re 
import numpy as np


def reWriteVector(vec):
    vec = re.sub(' +', ' ', vec) # removes eccess blank spaces
    vec = vec.replace(" ", ",") # replaces the last blank space with a comma
    vec = vec[1:] # removes the first character i.e. '['
    vec = vec[:-1] # same for the last ']'
    vec = [float(n) for n in vec[1:-1].split(",")] # creates list of floats from the string
    return vec

def reWriteMatrix(mat):
    mat = mat.replace('\n', "") # removes \n from the exp_mat matrix
    mat = re.sub(' +', ' ', mat) # removes eccess blank spaces
    mat = mat.replace(" ", ",") # replaces the last blank space with a comma
    #mat = mat.replace("[", "")
    #mat = mat.replace("]","")
    mat = mat[2:]
    mat = mat[:-1]
    #mat = re.sub("]", "]]", mat)
    #print(mat)
    rows = re.split("[\]\[]", mat)
    rows = list(filter((",").__ne__, rows))
    #print(rows)
    #matrix = np.zeros((len(rows),len(rows[1])))
    matriz = []
    for i in range(1,len(rows)-1):
        #matrix[i] = [float(n) for n in mat[1:-1].split(",")] # creates list of floats from the string
        row = rows[i]
        #print(i)
        #print(row,"hej")
        #row = row[1:] # removes the first character i.e. '['
        #row = row[:-1] # same for the last ']'
        row = row + ","
        matrix_row = [float(n) for n in row[1:-1].split(",")] # creates list of floats from the string
        #print(matrix_row)
        matriz.append(matrix_row)
    mat = matriz
    return mat

def generateMatrices(file_a, file_b, file_c, file_d):
    with open(file_b) as f: # Reads the entire file as one string
        content_b = f.read()

    with open(file_c) as f: # Reads the entire file as one string
        content_c = f.read()

    with open(file_d) as f:
        content_d = f.read()

    with open(file_a) as f:
        content_a = f.read()

    # Splits the text document into multiple strings with the different data
#    str1, gamma_vec_a, beta_vec_a, exp_mat_a, minima_a, coord_a, beta_vec_a, zz_a, zo_a, oz_a, oo_a = re.split(".+=", content_a)
    #str1, gamma_vec_a, beta_vec_a, exp_mat_a, minima_a, coord_a = re.split(".+=", content_a)
    str1, gamma_vec_a, beta_vec_a, exp_mat_a, minima_a, coord_a, str2, beta_vec_b, cost_vec_a, zz_a, zo_a, oz_a, oo_a, minima_a = re.split(".+=", content_a) # not correct, only went for correct number of terms
    str1, gamma_vec_b, beta_vec_b, exp_mat_b, minima_b, coord_b = re.split(".+=", content_b)

    str1, gamma_vec_c, beta_vec_c, exp_mat_c, minima_c, coord_c = re.split(".+=", content_c)

    str1, gamma_vec_d, beta_vec_d, exp_mat_d, minima_d, coord_d, str2, beta_vec_d, cost_vec_d, zz_d, zo_d, oz_d, oo_d, minima_d  = re.split(".+=", content_d)

    exp_mat_a = reWriteMatrix(exp_mat_a)
    exp_mat_b = reWriteMatrix(exp_mat_b)
    exp_mat_c = reWriteMatrix(exp_mat_c)
    exp_mat_d = reWriteMatrix(exp_mat_d)
    return exp_mat_a, exp_mat_b, exp_mat_c, exp_mat_d



if __name__ == "__main__":
    matplotlib.rcParams.update({'font.size': 12, 'text.usetex': True})

    with open("benchmarkDATA&PLOTS/Old_Data/plotdata_b_longrun.txt") as f: # Reads the entire file as one string
        content_b = f.read()

    with open("benchmarkDATA&PLOTS/Old_Data/plotdata_c_longrun2.txt") as f: # Reads the entire file as one string
        content_c = f.read()

    with open("benchmarkDATA&PLOTS/Old_Data/plotdata_d_longrun.txt") as f:
        content_d = f.read()

    with open("benchmarkDATA&PLOTS/Old_Data/plotdata_a_longrun.txt") as f:
        content_a = f.read()

    # Splits the text document into multiple strings with the different data
    str1, gamma_vec_a, beta_vec_a, exp_mat_a, minima_a, coord_a, beta_vec_a, zz_a, zo_a, oz_a, oo_a = re.split(".+=", content_a)

    str1, gamma_vec_b, beta_vec_b, exp_mat_b, minima_b, coord_b, beta_vec_b, zz_b, zo_b, oz_b, oo_b = re.split(".+=", content_b)

    str1, gamma_vec_c, beta_vec_c, exp_mat_c, minima_c, coord_c, beta_vec_c, zz_c, zo_c, oz_c, oo_c = re.split(".+=", content_c)

    str1, gamma_vec_d, beta_vec_d, exp_mat_d, minima_d, coord_d, beta_vec_d, zz_d, zo_d, oz_d, oo_d = re.split(".+=", content_d)

    '''Betaplot DATA'''
    cost_vec_a = [-0.013469406010308323, 0.021742574907017486, 0.05805494906946306, 0.09159157636220899, 0.12278294286310912, 0.1402469239718355, 0.1541005936432979, 0.15003992948645245, 0.1421030426966475, 0.11737008791234242, 0.08580807659754076, 0.04202289883207507, -0.005692025103326163, -0.06397589174387781, -0.12180535408153949, -0.1880248396192448, -0.2478846670064072, -0.3042482539754412, -0.3548176814722209, -0.39667774029479186, -0.4299582140187943, -0.4463731911149137, -0.44998251352728585, -0.4338849912733524, -0.4127018122587082, -0.37209023679084763, -0.3177916470459783, -0.25188778614431895, -0.17776799828405887, -0.0976361971036115, -0.011174045732954255, 0.07486926956276582, 0.15629071117174506, 0.23920617566856694, 0.313598292824919, 0.36477477874299724, 0.42682575095467107, 0.46188733096122697, 0.4836971867123217, 0.49432090609473633, 0.4866633856592028, 0.46828283756741607, 0.4303149255305712, 0.38542990338644667, 0.33106947150192567, 0.2722514701247685, 0.20724551122011328, 0.14165661740199084, 0.07785569590357597, 0.018430539805222333, -0.0339990894932966, -0.07727587821279995, -0.11381773879805641, -0.13594364240659582, -0.14473907203949515, -0.14874127149391514, -0.13607640500575047, -0.11579261780565864, -0.0880725192464514, -0.05397170094398979, -0.01733523974706899]
    zz_a = [0.24506983658295114, 0.2622342664051867, 0.27919849546062253, 0.2930545333367382, 0.3067465410694634, 0.3137166060890884, 0.3195543461588994, 0.3149888685261464, 0.3098837575997395, 0.29632364515083787, 0.27836347980186416, 0.2557155088659199, 0.23073446338147072, 0.2000935248917641, 0.17091410163520954, 0.13585274107516607, 0.10576467957367126, 0.07667223948596877, 0.05098290925500856, 0.030351773501173258, 0.013212340816069501, 0.006092100035353816, 0.003565768726605306, 0.01304074587619924, 0.02327402780094778, 0.04461529422870958, 0.07214064774098546, 0.10625679010973763, 0.14487740788464232, 0.1858668667656104, 0.22958837596728182, 0.27482536201567553, 0.31694461582019506, 0.3598549532873077, 0.39862342197563055, 0.4254422744848591, 0.4579951200939515, 0.47668391302326124, 0.49022988471673123, 0.4968849268358205, 0.49453976993347865, 0.487176260300202, 0.4686989616236364, 0.44683823489560304, 0.42082553776067066, 0.3927563561704258, 0.3611365970682503, 0.3278466491603678, 0.2966944852523471, 0.2676822546234584, 0.24100929972872512, 0.2185902339445417, 0.20038725484528447, 0.19037608153169286, 0.18467596131115102, 0.18196096962290545, 0.1878286248285171, 0.19677640655537396, 0.2099247265736357, 0.22636915895761697, 0.24328908550192377]
    zo_a = [0.2610040518407823, 0.21585059458928102, 0.17204706112630075, 0.1318357868526968, 0.0975913986021358, 0.06409994138188185, 0.04092175440956454, 0.017837173786544723, 0.007250434484861648, 0.002827951826423899, 0.00362144840760189, 0.013727335227781861, 0.03128559371597371, 0.05205946264455688, 0.07851936183093974, 0.1071993603296396, 0.1393449731713139, 0.1724290775224764, 0.2036428848109701, 0.23097996468438647, 0.25748403773484196, 0.27841648374352734, 0.2966341425056055, 0.3073936318117484, 0.31384472135970803, 0.313659123930941, 0.3079914467935224, 0.2990094163043155, 0.2851793223434991, 0.26887277050796693, 0.25104752194043206, 0.2320069868708327, 0.21188467506783024, 0.1961160065125782, 0.18312384888816888, 0.17358565386027075, 0.17089299710251754, 0.16985344168486108, 0.1755598639168392, 0.18826702210029528, 0.20518619201272206, 0.2275797122066798, 0.2536872559290522, 0.28410927154555393, 0.3150214271744411, 0.3472636617724804, 0.37803165292313656, 0.40878770015045574, 0.4349726441747144, 0.4541680984083216, 0.47143019784495516, 0.4797920592901606, 0.48251071029652803, 0.4749303734163002, 0.46448566994668866, 0.44349780745627915, 0.4162050579059324, 0.3847773258347608, 0.3466811822303686, 0.30458516583785705, 0.26078332346702493]
    oz_a = [0.258540229358503, 0.23725774903978605, 0.21626785376808766, 0.19956923600428947, 0.18398646816603292, 0.17345543378394188, 0.16544287486172915, 0.16497758376892938, 0.16778019969337854, 0.17884745166711796, 0.192559050423336, 0.21369561454530545, 0.23643055962228637, 0.26406875032895716, 0.2927078545037558, 0.3238741706833289, 0.35364582227651264, 0.38091617317141957, 0.4058008955291315, 0.42708597555724276, 0.44316490155275834, 0.4525123646869815, 0.4535428980105359, 0.44702238173509995, 0.4360237243004765, 0.41670004454684445, 0.38992591529267506, 0.3581668194536008, 0.3226419493695923, 0.28350009218716066, 0.2412498676469347, 0.19996417283443854, 0.16065127982133462, 0.12064623134169655, 0.08502335538693001, 0.060665656437967466, 0.03116901869021683, 0.014927574356075985, 0.0065321833630519275, 0.002564176511639003, 0.007876394637975846, 0.018889261301079954, 0.03838554739006183, 0.0614095399136745, 0.08975826545530646, 0.12050659553111698, 0.15387284503159834, 0.1861925471810783, 0.21884112381713328, 0.2492558916528165, 0.2749848087067755, 0.2957272186350307, 0.3142067459497359, 0.32631122265667434, 0.32941471720902765, 0.33070500383908485, 0.32378435963207924, 0.3125713065508235, 0.29794791883071253, 0.28016089666169686, 0.26062573612228]
    oo_a = [0.2353804183470332, 0.28018017878205226, 0.32265516196075805, 0.3680920745628251, 0.40964770720396293, 0.4486811195130589, 0.47387469634833435, 0.5020895402274234, 0.5150804293543187, 0.5217432496043068, 0.5254420623570816, 0.5168494070839993, 0.5015277102532609, 0.48377461844890995, 0.4577411735171762, 0.4328546156970098, 0.4012395025883714, 0.36996990527612633, 0.33955638065534766, 0.3114266022870179, 0.28613026016364357, 0.26289057980224867, 0.24624985417756068, 0.2324004387751569, 0.22678904098473596, 0.22501806274065678, 0.22993272890079403, 0.23653342746035996, 0.24729401596363176, 0.2617558662749099, 0.2776150324411603, 0.29318710352392874, 0.31051453770736087, 0.32337676511835944, 0.33322467033624903, 0.3403009827440849, 0.3399366072753631, 0.33835217293381076, 0.3276724017917385, 0.31227884520794147, 0.29239256077798786, 0.26634421097532723, 0.239220630178805, 0.20763702198845976, 0.17438830245432285, 0.13946838912399803, 0.10675636390372303, 0.07716812995189228, 0.049486574795415454, 0.028884498221479614, 0.012518250956172561, 0.00564373797425672, 0.0028886026171813252, 0.00836188510290259, 0.02141748861010713, 0.043831221889875836, 0.07204205145129607, 0.10586996145430769, 0.14538828367047418, 0.1886968426116997, 0.23529665460107146]

    cost_vec_b = [0.00817341564348339, -0.10302987385189888, -0.2049157245798137, -0.30784828398158476, -0.3993508614700884, -0.4910215353509475, -0.5754833695724094, -0.6625027780122525, -0.7280387243161033, -0.7934717991887258, -0.8477657679969252, -0.9027337716074237, -0.9283437362712602, -0.9648425001547639, -0.9859599784267771, -0.9764125344534053, -0.9878834302662266, -0.9655139637209665, -0.9300880808933191, -0.9075984713713865, -0.8577126147452878, -0.8023657311210529, -0.7374248124535748, -0.667550387982863, -0.5828355894739912, -0.5005801597306716, -0.4077148332434032, -0.3121547261805346, -0.21285100249490888, -0.1092157645067909, -0.011944763823527403, 0.09334049316778546, 0.20355551150903034, 0.29831281337864923, 0.3928052876607675, 0.48817144474113106, 0.5783907352863653, 0.6597063168293437, 0.7335369780681867, 0.7967281585535676, 0.853293911689021, 0.901966144728965, 0.943835285573258, 0.9615992579808172, 0.9890953570933916, 0.9877638290153606, 0.9836631384807238, 0.9751572593044676, 0.9487545077367027, 0.9075319347635645, 0.8633392186888957, 0.8053469277307761, 0.7439551752993909, 0.6663420033999328, 0.5826080888638598, 0.5066202633375658, 0.4179996165279964, 0.315093663763701, 0.21645062484134223, 0.11552250583400124, 0.01205990184870059]
    zz_b = [0.2538808088059001, 0.22442423106531215, 0.1981575884366896, 0.17005986549583435, 0.14480329666281452, 0.12047177463536415, 0.09935885898716201, 0.0781231791890136, 0.062452050560244846, 0.04705432009218614, 0.03452905992714485, 0.02200871911888317, 0.016466306466971347, 0.007921732499592098, 0.0032295060610051237, 0.00497948712228083, 0.0020132430193025978, 0.006302827607064691, 0.013341304294291678, 0.017274203568036724, 0.027226775288161333, 0.03831328943216576, 0.05157975113087995, 0.06617613042706853, 0.08432448693910848, 0.10227914409967971, 0.12314045813224948, 0.14522568276194828, 0.16847364537128948, 0.19372564354719332, 0.21842161687837938, 0.24558406335024074, 0.274747677418164, 0.301160151684267, 0.32818336123205977, 0.35675408815714016, 0.38318290244639414, 0.4086781633540029, 0.43183201970682594, 0.45390670302399655, 0.4726505417057799, 0.49089228141495844, 0.5061052133430918, 0.5154327135405232, 0.5264864740500066, 0.5289720414534217, 0.5304595415165273, 0.5297707757836146, 0.5242391544771583, 0.5135701242579322, 0.5004355245145635, 0.4852134290650466, 0.4673884690444176, 0.44561486391917565, 0.42071916439833557, 0.3982122039412957, 0.3724274292472037, 0.342978563476122, 0.3156354943665321, 0.2861928007532146, 0.2571947235678518]
    zo_b = [0.25020586352621577, 0.22547553617554955, 0.2029327239059553, 0.1790871782791833, 0.1565103726705588, 0.13407158651983678, 0.1129529080865397, 0.09065777746965863, 0.0735296931637849, 0.05622230683317048, 0.041591443298623486, 0.026626314950168862, 0.019364836498169752, 0.009658072544031521, 0.003791498749593674, 0.006815475424124802, 0.0040453179824646215, 0.010966333709998326, 0.021613897039245544, 0.028926415783742502, 0.043917034026081894, 0.06052709636330269, 0.07970776192055734, 0.10004925820422327, 0.12425756000527009, 0.14743085001712314, 0.1730026175541855, 0.1986970572089812, 0.22510116558344628, 0.2516668415268939, 0.27560608333369135, 0.30108655009329427, 0.3270303140616564, 0.34799641498078365, 0.36821962562620253, 0.3873317123743747, 0.4060126338604375, 0.42117523001876217, 0.4349363993393921, 0.4444575966672275, 0.4539965190800691, 0.4600907673920099, 0.4658126421015216, 0.4653668156314282, 0.46806129164552907, 0.46491006702502985, 0.46137193694989, 0.45780740863651703, 0.4501381962161247, 0.440195773394697, 0.43123403367106244, 0.4174574115174245, 0.4045891578608913, 0.3875555219492668, 0.37058203923251654, 0.35509640425426836, 0.3365724882425086, 0.31456830813943193, 0.29259365557677075, 0.2715673921950835, 0.24883528879419636]
    oz_b = [0.2555154623420831, 0.2777908594439681, 0.29631156382702195, 0.3185017867783404, 0.3394871596047348, 0.35667280607455565, 0.371211203763419, 0.38598025276701897, 0.39608648449575545, 0.4055386696110362, 0.4115527941647903, 0.4187671567047755, 0.4195846731891337, 0.42305015877214636, 0.4239466776741335, 0.41887311970243146, 0.41890314633459375, 0.41226501340874777, 0.40415589408832847, 0.3987364008751008, 0.38847406552412866, 0.37805907819120116, 0.3657757870246614, 0.35272054150082793, 0.3372360323390841, 0.3221637294759336, 0.30509609246081676, 0.2874550084772393, 0.2680265762544031, 0.24787303680397824, 0.22872094415676417, 0.20728299648829346, 0.18413010969791077, 0.1640112121227878, 0.1432927193768415, 0.12223206259014018, 0.10123946275043676, 0.08230150263332557, 0.06461351460665592, 0.04936339590780982, 0.035383539247820464, 0.023459860720044554, 0.013040348902303472, 0.008753119374941087, 0.0022294885207066796, 0.0029003792164814233, 0.004797830739147676, 0.007845954374909054, 0.01574114799065122, 0.02753916164078874, 0.04016980206366995, 0.056418313990541716, 0.07353502954682772, 0.09467695333078069, 0.1169797177403545, 0.13686559047916402, 0.1595940191301386, 0.18549584780359035, 0.21004526122038303, 0.23340556996094566, 0.2569333216545958]
    oo_b = [0.24039686183980236, 0.26764190164759694, 0.2923892057425784, 0.3247218735602607, 0.35715174226620705, 0.3887254480815532, 0.41629033661663745, 0.44514656254716667, 0.4679266698738712, 0.49114803762643056, 0.5123159068069645, 0.5325931382641031, 0.5445723895750314, 0.5593684195877241, 0.569029009971755, 0.5693275089218682, 0.5750374121962744, 0.5704356246328923, 0.560882530771454, 0.5550618636361385, 0.540378785109031, 0.5230769500983987, 0.5029354289856113, 0.4810527236912848, 0.45417764249077097, 0.42812368192687256, 0.3987595734930519, 0.36862168407573753, 0.3383976055706264, 0.3067338220001111, 0.27724952145616827, 0.2460453799337485, 0.21409142707326945, 0.18683039226140383, 0.16030355269716481, 0.13368018643971216, 0.1095640158461656, 0.08784406383895282, 0.06861623156723701, 0.05227153830679389, 0.03796844449069549, 0.025555950462972626, 0.01504113362548905, 0.010446038327587353, 0.0032219824549026875, 0.0032168502667351477, 0.003369644949728927, 0.004574239553096067, 0.009880752716648233, 0.01869400648134179, 0.028159702889346584, 0.0409066401725167, 0.054486614984602944, 0.0721510447217468, 0.09171504437277611, 0.1098234060102309, 0.131405277561973, 0.15695653162409526, 0.1817211304661598, 0.20883223719612196, 0.2370359725003864]

    cost_vec_c = [0.013518470282559846, -0.09505627606140157, -0.19976091214962133, -0.30194868385412155, -0.3944387660471152, -0.48592455847663446, -0.5672014099761732, -0.6514988270600677, -0.7256370644724245, -0.7884331326894866, -0.8466060316743772, -0.8957406229993642, -0.936389972526074, -0.9650953257453833, -0.9834710404515117, -0.9880580734492977, -0.9809973658994285, -0.9723576767859508, -0.9394260607525758, -0.9076407881375747, -0.8616222533285106, -0.8055906871471443, -0.7429752509586977, -0.6661143932001601, -0.5876572454046382, -0.5039620869917653, -0.41150745620341106, -0.3146253766949948, -0.21463520116876844, -0.11109569738568226, -0.007936098300372233, 0.09476254789645219, 0.19419232411060053, 0.2985113871374823, 0.3978219627564545, 0.48953573022649166, 0.5745803318491032, 0.6560553207963778, 0.7312188320075126, 0.8010285892389075, 0.854509833490285, 0.9050639280443904, 0.9427977043357992, 0.9702524279111531, 0.9866815401223126, 0.9965292201769664, 0.9884380807719342, 0.97287118320324, 0.94673337073018, 0.9141913531980682, 0.8685075137799281, 0.8143813296303334, 0.7500695402728006, 0.6733081273028888, 0.5953322612219133, 0.5100214881136415, 0.4190865867635074, 0.32235967247805053, 0.2232919935637268, 0.1188877045442863, 0.016695132366342947]
    zz_c = [0.25391591901099164, 0.20397963267341618, 0.16166817586851273, 0.12216754449885386, 0.08990612338671412, 0.06367635682696636, 0.044662700247332224, 0.028458399312741137, 0.017235872942642068, 0.009886212955101982, 0.004861791078507025, 0.0019963763627773887, 0.0005671844370585295, 9.401170557499035e-05, 5.706531809076665e-05, 0.00013483201173473993, 0.00026288088906054063, 0.00038903287184170943, 0.0010608400633964267, 0.0021953568692824055, 0.004702389046418968, 0.009195103512302651, 0.016022598709497488, 0.027141408930664072, 0.041514053294632064, 0.060278065428647554, 0.08507572384074046, 0.11570847900440971, 0.15211703922807612, 0.19546089776532802, 0.24386364021925458, 0.2974089889602846, 0.35430246545374494, 0.4193861225192312, 0.4864321643604609, 0.5528258315076338, 0.6181269675065607, 0.6841854379240341, 0.7480969428255496, 0.8099993610240068, 0.8591230226532407, 0.9068904575654809, 0.9433970985783606, 0.9704293781459241, 0.9868071014536137, 0.9966903116380897, 0.9886359512445805, 0.97320701749872, 0.9474609826049879, 0.9158903324260277, 0.8724600039040598, 0.822370182576449, 0.7647681680486789, 0.6987483997060676, 0.6347053809240832, 0.5681960557588134, 0.5012778903717646, 0.43470004856753847, 0.37144295725300214, 0.3101139375079973, 0.25544322408003783]
    zo_c = [0.2501707506272174, 0.247178010906827, 0.24107150344511308, 0.22711780547037003, 0.21068680033851173, 0.1898501370140472, 0.17050378895450974, 0.14446859413992222, 0.11735135128611895, 0.09474075044146946, 0.07103744799431275, 0.05029754113787672, 0.029011578352231, 0.01633161780723971, 0.005926133555941166, 0.005721576879929529, 0.010701727896918948, 0.011848606653454831, 0.029497511812383335, 0.044181502307720194, 0.06481298823089963, 0.0885021163916565, 0.11242178970245678, 0.14199934323623745, 0.1662210012887083, 0.1879852159122043, 0.20970149276666034, 0.2277791130044095, 0.2412929017661357, 0.250558746948784, 0.25428913233077954, 0.2515799302756777, 0.24165006484571916, 0.2305461199142456, 0.21403665578429434, 0.19273635024769378, 0.1684119992847868, 0.14441736911749084, 0.1169975458390769, 0.09157947397520766, 0.0669772578242647, 0.04548065482256128, 0.028594028682901763, 0.01356089498047392, 0.0046952967802651934, 0.002135222433809882, 0.0030148906807125294, 0.011692168999265829, 0.02443248468760883, 0.04021189207766355, 0.05994754666261811, 0.0835222668834854, 0.10889134955805271, 0.13428533359274014, 0.16026460711859963, 0.18455462128232514, 0.20641212005405804, 0.2245608738610234, 0.237974171260812, 0.24672126862365795, 0.25117003219914324]
    oz_c = [0.2555161336716304, 0.2523919292006451, 0.2423195429012947, 0.23231553795453652, 0.21699862028416056, 0.19698141656793722, 0.1730872963351364, 0.14720432401912387, 0.12254276832914325, 0.09708754833220172, 0.07264711879976142, 0.04997257047350851, 0.03347732112235854, 0.01838790220090512, 0.01049183094741635, 0.005956567093976455, 0.007776167843517062, 0.015018415843714251, 0.02896368207978, 0.04378726079842274, 0.06416235652055403, 0.08751968593802106, 0.11255832821311583, 0.13760538243864412, 0.1631174566378279, 0.18749850451088532, 0.20864153263238513, 0.2261788760693473, 0.23983877976243415, 0.24742509350559744, 0.25004793364620764, 0.24836610671574652, 0.24393900738385607, 0.22919350649200862, 0.2109215971234394, 0.1911546546259969, 0.1699149726485747, 0.14326746887536634, 0.1180277614754443, 0.089450654021706, 0.06928674475307812, 0.04580324964043445, 0.027409663695578745, 0.015832914963754958, 0.008372158169875262, 0.0010134706754621474, 0.008151388985355789, 0.014765975253377172, 0.02737962930431933, 0.04219895737841286, 0.06364001739043466, 0.08611876188385431, 0.11164192330484442, 0.14152641484626083, 0.16565699482037963, 0.18907486325227107, 0.210118827963153, 0.22839896902279014, 0.24243272952524783, 0.251939965233291, 0.2546390132389696]
    oo_c = [0.2403964153634181, 0.2916814503093177, 0.3439952990554068, 0.4095213872013776, 0.47960862555071104, 0.5493466495846799, 0.6115935990117187, 0.6797566299406765, 0.742865130523664, 0.7982465879452212, 0.8514377531966705, 0.8977290081505921, 0.9369298432229298, 0.9651833880363533, 0.9835216987698214, 0.9881809834354164, 0.9812577218028019, 0.9727411488258865, 0.9404687134635368, 0.9098355531783268, 0.86631984095385, 0.814779897639957, 0.7589967100448691, 0.6932517440652138, 0.6291175772665523, 0.5642361442596348, 0.49657902217972155, 0.43033317276333827, 0.3667500722832441, 0.30655314916783005, 0.251798746270554, 0.20264308774169879, 0.16010654518861592, 0.12087347461875016, 0.08860848249577077, 0.06325664818762164, 0.04354496800757613, 0.028128661983510408, 0.016876943687639014, 0.008969645850231394, 0.004612263998404596, 0.0018238979426205173, 0.0005983722360379486, 0.000176070233749403, 0.00012466439986119442, 0.0001602335986395499, 0.00019694392217971352, 0.0003264066018897673, 0.0007242206057448034, 0.0016977140835849655, 0.003951681393037062, 0.007987968250383493, 0.014697845609681074, 0.0254363525753321, 0.03937219796564292, 0.05817368158283699, 0.08219031306754729, 0.11233806698553758, 0.14814662772450538, 0.19122145834161136, 0.23874541131134874]

    cost_vec_d = [-0.06856888810857546, 0.13794217548625112, 0.34266931435437625, 0.5261142475914308, 0.6914849982303, 0.8185283896971949, 0.9206782163644355, 0.9749261038310157, 0.9915674155615447, 0.9606172163683547, 0.8987052161413962, 0.7812412979380949, 0.6416607768154077, 0.472916011666209, 0.28299655057762024, 0.0823718049161786, -0.12306754039564857, -0.3215896935618913, -0.5077155784895699, -0.6700795961837419, -0.7995312604072953, -0.9022911789291149, -0.9540378864338952, -0.9641871695796431, -0.9386779565909351, -0.8671499424465229, -0.7592173818631822, -0.6193925651632474, -0.4489958786447496, -0.2587643535990017, -0.05383181462461075, 0.1491107307311646, 0.3453146551846139, 0.5308073116990927, 0.6915228524244005, 0.8242609046323774, 0.9220508913060387, 0.9754271895539682, 0.9953725266845166, 0.9617080461622906, 0.8869856788049019, 0.7809425996822968, 0.6361843055339214, 0.46086973262391495, 0.2698842565461412, 0.06911267000955047, -0.1380515480773901, -0.33529174316598276, -0.5196029447177564, -0.68017334872136, -0.819241102901452, -0.9193955070753064, -0.9753433729217462, -0.9874021569152587, -0.959851249282588, -0.891529634472331, -0.7844628705688603, -0.6408193408825564, -0.4693094400462886, -0.2776016236779596, -0.07317881070535791]
    zz_d = [0.23758216133241772, 0.2878042595671786, 0.3388268633496841, 0.38547748119168296, 0.42793699458096307, 0.46011052035729244, 0.4854823594262414, 0.5009035328197581, 0.5033573655023659, 0.4950476224618276, 0.47997255921121895, 0.4508493803830738, 0.41555106728850305, 0.37311651411753227, 0.32354593499366535, 0.2739810139707472, 0.22292806910595708, 0.17330911747883598, 0.1243818760556761, 0.08440522595486467, 0.05072726305027855, 0.02508293279649721, 0.011754235805040104, 0.007863444118511349, 0.013863000747142284, 0.03177752718528853, 0.058226505872036025, 0.0923371365979274, 0.1340294694863572, 0.182073794525528, 0.23258271334805056, 0.28276235639788366, 0.3289594449727955, 0.377230740385807, 0.4178374741935877, 0.45073460128759496, 0.47397368483388413, 0.48903396057204584, 0.4945730364239892, 0.4861503728577434, 0.4669846267346958, 0.43967644354036006, 0.40455869749809364, 0.36098763328195094, 0.31229008677230174, 0.26370774457195434, 0.21312984732116877, 0.16296348007312655, 0.11790122575701924, 0.07752136293428813, 0.04450472678312813, 0.019141648655729725, 0.0065408361032802485, 0.003401713227916993, 0.00965240488056014, 0.02866629815635249, 0.05597291378516985, 0.0932410240207904, 0.13553937132406374, 0.1844254537000161, 0.23771624245192863]
    zo_d = [0.2697326217317009, 0.21519988090680256, 0.16473274946094135, 0.1212692744780375, 0.07852586006271543, 0.04658836229426294, 0.020924708882258402, 0.006643773834453727, 0.0028590505605855005, 0.009691619663305185, 0.024929341656940537, 0.0539519798225412, 0.0888014066913338, 0.13020828987377, 0.1794664515529652, 0.22854385828911034, 0.27997584325209685, 0.32807179973878, 0.37660968757707924, 0.4158070484979053, 0.4471802740892482, 0.4742596630489124, 0.48670369303040933, 0.48978980691515334, 0.4806939179722212, 0.46494160578726684, 0.4395974066684001, 0.40361357656694347, 0.3608561626781448, 0.313579567437342, 0.26288033592465676, 0.21131869905451647, 0.16018509657376356, 0.11598470214271017, 0.0770261482199136, 0.04463785707219398, 0.018866333764633363, 0.005635358935532567, 0.00045046315458266656, 0.009193019675034286, 0.02785044287737289, 0.055651882834849016, 0.09164544224561115, 0.13647842166299148, 0.18417200108262002, 0.23384130900614986, 0.28415533302927615, 0.33558891960819853, 0.3802406343348637, 0.4208159398670614, 0.4557831893847602, 0.48125074081558844, 0.4950901336112481, 0.5009465742784179, 0.49099882295644104, 0.47366928345732107, 0.4486134550822887, 0.4125852064898335, 0.36875606490649715, 0.3204267247171718, 0.27150672237375373]
    oz_d = [0.2645501906083525, 0.21375597031882496, 0.16224913796517437, 0.1162559232554425, 0.07623439281588708, 0.044050707156103715, 0.018792319317806738, 0.005943875676076813, 0.0013508870965667054, 0.009295890338822384, 0.025719086796699937, 0.05512859814975333, 0.09034130508199524, 0.13270773987609163, 0.17904175381167012, 0.23027256945409968, 0.2814574930182517, 0.33272679555788204, 0.37724868386828636, 0.41923457234041916, 0.45258723182674054, 0.47688689659516165, 0.490330650604692, 0.4922844960694623, 0.4886462360625732, 0.4687729456524737, 0.4402034924663141, 0.4065274212990578, 0.3636411573785181, 0.31580384445299947, 0.2646207954555657, 0.21412507903305186, 0.16719057101763246, 0.11869811662222018, 0.07762036167296348, 0.043512539511599835, 0.020105496989927554, 0.006648906089131649, 0.0018599225325647906, 0.009949716162496049, 0.028708566529068755, 0.053873148051430356, 0.09025838193257033, 0.1330827737494652, 0.18062466966295454, 0.2314617752531226, 0.2848108548764225, 0.3320376723662607, 0.37935948946794545, 0.41880809985950884, 0.4538464634204346, 0.47844351954953396, 0.49257710924044934, 0.4927508210347215, 0.48856015151504595, 0.4720923540273435, 0.4433150239955976, 0.4078221148334936, 0.36544431930999005, 0.3183715846630805, 0.26477111950897275]
    oo_d = [0.22813236740181814, 0.27858093620136926, 0.3239248421614115, 0.36913304524432555, 0.41499141924436406, 0.4491338168225818, 0.4746347492660414, 0.48643047352974317, 0.49242392779138827, 0.48539715456304955, 0.4693707825328122, 0.4397882816566954, 0.40525292986108913, 0.3632048273539379, 0.3179373590882393, 0.2671975787971319, 0.21535594470177072, 0.16588662043957486, 0.12175570279415643, 0.0805476814163676, 0.04950163748291227, 0.023767213565119055, 0.011180131252716687, 0.01004422093271656, 0.016792680939805328, 0.034285175775849296, 0.061746593849273355, 0.09703295244289818, 0.1414703990719156, 0.1885384887841972, 0.23932405681394972, 0.2917908530459263, 0.34362667415334247, 0.38798705803448785, 0.42704298448604994, 0.4607581482175982, 0.4870517381322035, 0.4986779920917636, 0.5031140570081161, 0.4947039928398184, 0.47622386901198793, 0.45079600181157936, 0.4135343922688787, 0.369447540155249, 0.3221396042153757, 0.2707175033157619, 0.21781801914578713, 0.16939392182569685, 0.12229044614125754, 0.08243297694633193, 0.045848241305807336, 0.021161504492687853, 0.00578859663614538, 0.0028980498834719945, 0.010574569050708221, 0.025569272394445876, 0.0519356247363256, 0.08634908556653434, 0.1300133707456907, 0.17677329330135078, 0.2258483284953329]


    gamma_vec_a = reWriteVector(gamma_vec_a)
    beta_vec_a = reWriteVector(beta_vec_a)
    exp_mat_a = reWriteMatrix(exp_mat_a)

    gamma_vec_b = reWriteVector(gamma_vec_b)
    beta_vec_b = reWriteVector(beta_vec_b)
    exp_mat_b = reWriteMatrix(exp_mat_b)

    gamma_vec_c = reWriteVector(gamma_vec_c)
    beta_vec_c = reWriteVector(beta_vec_c)
    exp_mat_c = reWriteMatrix(exp_mat_c)

    gamma_vec_d = reWriteVector(gamma_vec_d)
    beta_vec_d = reWriteVector(beta_vec_d)
    exp_mat_d = reWriteMatrix(exp_mat_d)

    gamma_vec = gamma_vec_b
    beta_vec = beta_vec_b

    # plotting matrix
    # plt.matshow(exp_mat, cmap = plt.get_cmap('PiYG'))  # We need to flip the matrix of we use the matshow
    # Do this by putting exp_mat[beta_resolution-1-j, i] = np.mean(expect(ham, state)) in for loops!) !
    fig, ax = plt.subplots(2,2, tight_layout = False)
    cs_a = ax[0,0].contourf(gamma_vec_a, beta_vec_a, exp_mat_a, 400, cmap=plt.get_cmap('PiYG'), vmin=-1, vmax=1, levels=np.linspace(-1,1,345))
    cs_b = ax[0,1].contourf(gamma_vec_b, beta_vec_b, exp_mat_b, 400, cmap=plt.get_cmap('PiYG'), vmin=-1, vmax=1, levels=np.linspace(-1,1,345))
    cs_c = ax[1,0].contourf(gamma_vec_c, beta_vec_c, exp_mat_c, 400, cmap=plt.get_cmap('PiYG'), vmin=-1, vmax=1, levels=np.linspace(-1,1,345))
    cs_d = ax[1,1].contourf(gamma_vec_d, beta_vec_d, exp_mat_d, 400, cmap=plt.get_cmap('PiYG'), vmin=-1, vmax=1, levels=np.linspace(-1,1,345))
    # This one plots the matrix with angles

    labels = ["0", "$\pi$/2", "$\pi$"]
    cbar = fig.colorbar(cs_b, ticks=np.linspace(-1,1,9), ax=ax)
    ticks = [gamma_vec[0], (gamma_vec[-1] + gamma_vec[0])/2, gamma_vec[-1]]
    #plt.setp(ax, xticks=ticks, xticklabels=labels, yticks=ticks, yticklabels=labels)
    plt.setp(ax[0,0], xticks=ticks, xticklabels=[], yticks=ticks, yticklabels=labels)
    plt.setp(ax[0,1], xticks=ticks, xticklabels=[], yticks=ticks, yticklabels=[])
    plt.setp(ax[1,0], xticks=ticks, xticklabels=labels, yticks=ticks, yticklabels=labels)
    plt.setp(ax[1,1], xticks=ticks, xticklabels=labels, yticks=ticks, yticklabels=[])
    
    

    #ax[0,0].set_title(f'Cost function F($\gamma$, \u03B2) for problem a')
    #ax[0,0].set_ylabel("\u03B2$_1$")
    ax[0,0].set_ylabel(r"$\beta_1$")    
    #plt.xticks([gamma_vec[0], (gamma_vec[-1] + gamma_vec[0])/2, gamma_vec[-1]], labels)
    #plt.yticks([gamma_vec[0], (gamma_vec[-1] + gamma_vec[0])/2, gamma_vec[-1]], labels)
    ax[0,0].text(0.05, 0.85, r'$\textbf{(a)}$', fontsize = 18, weight='bold', transform=ax[0,0].transAxes)

    #ax[0,1].set_title(f'Cost function F($\gamma$, \u03B2) for problem b')
    ax[0,1].text(0.05,0.85, r'$\textbf{(b)}$', fontsize = 18, weight='bold', transform=ax[0,1].transAxes)
    #plt.xticks([gamma_vec[0], (gamma_vec[-1] + gamma_vec[0])/2, gamma_vec[-1]], labels)
    #plt.yticks([gamma_vec[0], (gamma_vec[-1] + gamma_vec[0])/2, gamma_vec[-1]], labels)

    #ax[1,0].set_title(f'Cost function F($\gamma$, \u03B2) for problem c')
    ax[1,0].set_xlabel("$\gamma_1$")
    #ax[1,0].set_ylabel("\u03B2$_1$")
    ax[1,0].set_ylabel(r"$\beta_1$")
    ax[1,0].text(0.05, 0.85, r'$\textbf{(c)}$', fontsize = 18, weight='bold', transform=ax[1,0].transAxes)
    #plt.xticks([gamma_vec[0], (gamma_vec[-1] + gamma_vec[0])/2, gamma_vec[-1]], labels)
    #plt.yticks([gamma_vec[0], (gamma_vec[-1] + gamma_vec[0])/2, gamma_vec[-1]], labels)

    #ax[1,1].set_title(f'Cost function F($\gamma$, \u03B2) for problem d')
    ax[1,1].set_xlabel("$\gamma_1$")
    ax[1,1].text(0.05, 0.85, r'$\textbf{(d)}$', fontsize = 18, weight='bold', transform=ax[1,1].transAxes)
    #plt.xticks([gamma_vec[0], (gamma_vec[-1] + gamma_vec[0])/2, gamma_vec[-1]], labels)
    #plt.yticks([gamma_vec[0], (gamma_vec[-1] + gamma_vec[0])/2, gamma_vec[-1]], labels)

    plt.show()
    fig.savefig("benchmarkplot.png", format="png", bbox_inches="tight")

    #coord_a = [22, 16]
    #coord_b = [44, 44]
    #coord_c = [15, 28]
    #coord_d = [37, 44]

    #cost_vec_a = [cost[coord_a[1]] for cost in exp_mat_a]
    #cost_vec_b = [cost[coord_b[1]] for cost in exp_mat_b]
    #cost_vec_c = [cost[coord_c[1]] for cost in exp_mat_c]
    #cost_vec_d = [cost[coord_d[1]] for cost in exp_mat_d]


    fig2, ax2 = plt.subplots(2,2)
    """
    for i in ax2[0,:]:
        for j in ax2[1,:]:
            print(j)
            handles, labels = j.get_legend_handles_labels()
            print(handles)
            print(labels)
            #j.legend(handles, labels, loc='upper center')
    """
    beta_vec = np.linspace(0,np.pi,61)
    ax2[0,0].set(xlim= (0,np.pi), ylim= (-1, 1))

    ax2[0,0].plot(beta_vec, cost_vec_a, 'o',markerfacecolor='none', markeredgecolor ="magenta", label="$F$")
    ax2[0,0].plot(beta_vec, zz_a, 'o',markerfacecolor='none', markeredgecolor ="orange", label=r"$P_{|00\rangle}$")
    ax2[0,0].plot(beta_vec, zo_a, 'o',markerfacecolor='none', markeredgecolor ="red", label=r"$P_{|01\rangle}$")
    ax2[0,0].plot(beta_vec, oz_a, 'o',markerfacecolor='none', markeredgecolor ="green", label=r"$P_{|10\rangle}$")
    ax2[0,0].plot(beta_vec, oo_a, 'o',markerfacecolor='none', markeredgecolor ="purple",  label=r"$P_{|11\rangle}$")

    ax2[0,0].text(0.05, 0.85, r'$\textbf{(a)}$', fontsize = 18, weight='bold', transform=ax2[0,0].transAxes)

    #ax2[0,0].set_xlabel(r"$\beta$")
    ax2[0,0].set_ylabel("$F,P$")


    #cost_vec_b.reverse() # reverses the list
    #zz_b.reverse()
    #zo_b.reverse()
    #oz_b.reverse()
    #oo_b.reverse()

    ax2[0,1].plot(beta_vec, cost_vec_b, 'o',markerfacecolor='none', markeredgecolor ="magenta", label="F")
    ax2[0,1].plot(beta_vec, zz_b, 'o',markerfacecolor='none', markeredgecolor ="orange", label="P(|00>)")
    ax2[0,1].plot(beta_vec, zo_b, 'o',markerfacecolor='none', markeredgecolor ="red", label="P(|01>)")
    ax2[0,1].plot(beta_vec, oz_b, 'o',markerfacecolor='none', markeredgecolor ="green", label="P(|10>)")
    ax2[0,1].plot(beta_vec, oo_b, 'o',markerfacecolor='none', markeredgecolor ="purple",  label="P(|11>)")

    ax2[0,1].text(0.05, 0.85, r'$\textbf{(b)}$', fontsize = 18, weight='bold', transform=ax2[0,1].transAxes)

    ax2[1,0].plot(beta_vec, cost_vec_c, 'o',markerfacecolor='none', markeredgecolor = "magenta", label="F")
    ax2[1,0].plot(beta_vec, zz_c, 'o',markerfacecolor='none', markeredgecolor = "orange", label="P(|00>)")
    ax2[1,0].plot(beta_vec, zo_c, 'o',markerfacecolor='none', markeredgecolor ="red", label="P(|01>)")
    ax2[1,0].plot(beta_vec, oz_c, 'o',markerfacecolor='none', markeredgecolor ="green", label="P(|10>)")
    ax2[1,0].plot(beta_vec, oo_c, 'o',markerfacecolor='none', markeredgecolor ="purple",  label="P(|11>)")
    ax2[1,0].set_xlabel(r"$\beta$")
    ax2[1,0].set_ylabel("$F,P$")


    ax2[1,0].text(0.05, 0.05, r'$\textbf{(c)}$', fontsize = 18, weight='bold', transform=ax2[1,0].transAxes)

    #cost_vec_d.reverse()
    #zz_d.reverse()
    #zo_d.reverse()
    #oz_d.reverse()
    #oo_d.reverse()

    ax2[1,1].plot(beta_vec, cost_vec_d, 'o',markerfacecolor='none', markeredgecolor ="magenta", label="F")
    ax2[1,1].plot(beta_vec, zz_d, 'o',markerfacecolor='none', markeredgecolor ="orange", label="P(|00>)")
    ax2[1,1].plot(beta_vec, zo_d, 'o',markerfacecolor='none', markeredgecolor ="red", label="P(|01>)")
    ax2[1,1].plot(beta_vec, oz_d, 'o',markerfacecolor='none', markeredgecolor ="green", label="P(|10>)")
    ax2[1,1].plot(beta_vec, oo_d, 'o',markerfacecolor='none', markeredgecolor ="purple",  label="P(|11>)")
    ax2[1,1].set_xlabel(r"$\beta$")

    ax2[1,1].text(0.05, 0.05, r'$\textbf{(d)}$', fontsize = 18, weight='bold', transform=ax2[1,1].transAxes)

    #ax2.legend()
    #ax2.set(xlim= (0,pi), ylim= (-1, 1))
    #Title if you want, uncomment then
    #ax2.set_title('Problem {problem}')
    #ax2.set_xlabel(r"$\beta$")
    #ax2.set_ylabel("Cost function or probability of occupation")

    xticks = [gamma_vec[0], (gamma_vec[-1] + gamma_vec[0])/2, gamma_vec[-1]]
    yticks = [-1,0,1]
    xlabels = ["0", "$\pi$/2", "$\pi$"]
    ylabels = ["-1", "0", "1"]
    #plt.setp(ax2, xticks=xticks, xticklabels=xlabels,yticks=yticks, yticklabels=ylabels) #,yticks=yticks, yticklabels=ylabels)
    plt.setp(ax2[0,0], xticks=xticks, xticklabels=[],yticks=yticks, yticklabels=ylabels) #,yticks=yticks, yticklabels=ylabels)
    plt.setp(ax2[0,1], xticks=xticks, xticklabels=[],yticks=yticks, yticklabels=[]) #,yticks=yticks, yticklabels=ylabels)
    plt.setp(ax2[1,0], xticks=xticks, xticklabels=xlabels,yticks=yticks, yticklabels=ylabels) #,yticks=yticks, yticklabels=ylabels)
    plt.setp(ax2[1,1], xticks=xticks, xticklabels=xlabels,yticks=yticks, yticklabels=[]) #,yticks=yticks, yticklabels=ylabels)


    """
    #handles, labels = ax2[1,1].get_legend_handles_labels()
    ax2[0,0].legend(loc='center')
    ax2[0,1].legend(loc='center')
    ax2[1,0].legend(loc='center')
    ax2[1,1].legend(loc='center')
    """
    handles, labels = ax2[0,0].get_legend_handles_labels()
    fig2.legend(handles, labels, loc='upper center',ncol=5)

    plt.show()
    fig.savefig("betaplotbenchmark.png", format="png", bbox_inches="tight")
    fig.savefig("betaplotbenchmark.pdf", format="pdf", bbox_inches="tight")
