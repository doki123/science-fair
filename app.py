from flask import *
from werkzeug.utils import secure_filename
import os
import cv2
from joblib import load

app = Flask('Shop')
app.config['UPLOAD_FOLDER'] = 'static/images'
pic_label = {}
apple_variety_translate = {'Apple Braeburn': 'Braeburn', 'Apple Golden 1': 'Golden Delicious',
                           'Apple Golden 2': 'Golden Delicious', 'Apple Golden 3': 'Golden Delicious',
                           'Apple Granny Smith': 'Granny Smith', 'Apple Pink Lady': 'Pink Lady',
                           'Apple Red Delicious': 'Red Delicious', 'Apple Red 1': 'Honey Crisp',
                           'Apple Red 2': 'Honey Crisp', 'Apple Red 3': 'Honey Crisp', 'Apple Red Yellow 1': 'Red Gold',
                           'Apple Red Yellow 2': 'Red Gold'}
# syntax: apple_name = {'use like baking': [['name of recipe', 'recipe link'], ['name of recipe', 'recipe_link']], etc}
braeburn = {
    'baking': [['Apple Pie With Cinnamon Crust',
                'https://www.readyseteat.com/recipes-Braeburn-Apple-Pie-with-Cinnamon-Infused-Crust-3819'],
               ['Cupcakes', 'https://eatsmarter.com/recipes/braeburn-cupcakes'],
               ['Baked Apples', 'https://www.aldi.co.uk/baked-braeburn-apples/p/000000188154100']],
    'sauce': [['Applesauce', 'https://www.marthastewart.com/872914/classic-applesauce']]}
golden_delicious = {
    'baking': [['Apple Pie', 'https://www.allrecipes.com/recipe/12526/apple-pie-ii/'],
               ['Apple Sausage Casserole',
                'https://www.allrecipes.com/recipe/216392/sausage-and-apple-breakfast-casserole/'],
               ['Thanksgiving Stuffing',
                'https://www.allrecipes.com/recipe/13651/awesome-sausage-apple-and-cranberry-stuffing/']],
    'sauce': [['Apple Butter', 'https://www.allrecipes.com/recipe/139341/slow-cooker-apple-butter/'],
              ['Salsa and Chips', 'https://www.allrecipes.com/recipe/26692/annies-fruit-salsa-and-cinnamon-chips/'],
              ['Applesauce',
               'https://www.bettycrocker.com/recipes/homemade-cinnamon-applesauce/ee06c3d6-8780-4aed-bfda-37cae5d161fe']
              ]}
granny_smith = {
    'baking': [['Apple Pie', 'https://www.allrecipes.com/recipe/12682/apple-pie-by-grandma-ople/'],
               ['Apple Turnovers', 'https://www.allrecipes.com/recipe/59124/apple-turnovers/'],
               ['Butternut Apple Soup', 'https://www.allrecipes.com/recipe/149141/butternut-and-apple-harvest-soup/'],
               ['Apple Dumplings', 'https://www.allrecipes.com/recipe/46232/old-fashioned-apple-dumplings/']],
    'sauce': [['Applesauce', 'https://www.thespruceeats.com/homemade-applesauce-recipe-parve-2122354'],
              ['Cranberry Apple Sauce', 'https://www.allrecipes.com/recipe/267958/cranberry-sauce-with-apples/']],
    'beverages': [['Apple Cider Vinaigrette',
                   'https://www.epicurious.com/recipes/food/views/granny-smith-apple-cider-vinaigrette-51125210'],
                  ['Apple Cider', 'https://tasty.co/recipe/homemade-apple-cider']]}
pink_lady = {
    'baking': [['Bread Pudding',
                'https://pinkladyamerica.org/recipe/pink-lady-bread-pudding-with-cinnamon-bourbon-sauce/'],
               ['Apple Tart', 'https://pinkladyamerica.org/recipe/apple-tart-with-vanilla-bean-creme-anglaise/'],
               ['Apple Pancake', 'https://pinkladyamerica.org/recipe/pink-lady-apple-dutch-baby-pancake/']],
    'sauce': [['Cinnamon Apple Sauce',
               'https://www.fifteenspatulas.com/pink-lady-apple-sauce-with-cardamom-and-cinnamon/'],
              ['Curried Apple Sauce', 'https://theprimaldesire.com/curried-apple-sauce/']]}
red_delicious = {
    'sauce': [['Applesauce', 'https://www.thedailymeal.com/recipes/easy-slow-cooker-apple-sauce-recipe'],
              ['Cranberry Apple Sauce', 'https://www.savoryexperiments.com/10-minute-cran-apple-sauce/'],
              ['Spiced Carrot Apple Sauce', 'https://kiipfit.com/spiced-apple-carrot-soup/']]}
honey_crisp = {
    'baking': [['Apple Tart', 'https://www.theredheadbaker.com/honeycrisp-apple-tart-sundaysupper/'],
               ['Apple Crumble', 'https://www.theredheadbaker.com/honeycrisp-apple-crumble/'],
               ['Apple Parsnip Soup',
                'https://cooking.nytimes.com/recipes/12971-honeycrisp-apple-and-parsnip-soup?mcubz=1'],
               ['Apple Bread', 'https://mealplannerpro.com/member-recipes/Honeycrisp-Apple-Bread-232434'],
               ['Caramel Apple Bars', 'http://www.lilcelebrations.com/2015/10/caramel-honeycrisp-apple-bars/']],
    'sauce': [['Apple Hummus', 'https://turniptheoven.com/honeycrisp-apple-hummus/'],
              ['Apple Cranberry Sauce',
               'https://peasandcrayons.com/2014/11/slow-cooker-apple-strawberry-cranberry-sauce.html'],
              ['Applesauce', 'https://howdoyoufood.com/honeycrisp-applesauce/']],
    'beverages': [['Apple Sangria', 'https://tastykitchen.com/recipes/drinks/honeycrisp-apple-sangria/'],
                  ['Apple Cider Rum Punch', 'https://thissillygirlskitchen.com/honeycrisp-apple-cider-rum-punch/']]}
red_gold = {
    'sauce': [['Pink Hued Apple Jam',
               'https://cookpad.com/us/recipes/155471-pink-hued-apple-jam-using-red-gold-apples'],
              ['Applesauce', 'https://www.culinaryhill.com/applesauce-recipe/']],
    'beverages': [['Spiced Red Wine Apples',
                   'https://cookingontheweekends.com/spiced-red-wine-crimson-gold-apples-with-vanilla-mascarpone/']]}
# label_list = []
label_list_full = []
apple_variety_uses = {'Braeburn': braeburn, 'Golden Delicious': golden_delicious, 'Granny Smith': granny_smith,
                      'Pink Lady': pink_lady, 'Red Delicious': red_delicious, 'Honey Crisp': honey_crisp,
                      'Red Gold': red_gold}


@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'GET':
        apple_pic = os.listdir('static/images')
        return render_template('apple_index.html', apple_pic=apple_pic, pic_label=pic_label,
                               apple_variety_uses=apple_variety_uses, label_list=set(label_list_full)
                               , honey_crisp=honey_crisp)

    if request.method == 'POST':
        if 'delete_one' in request.form:
            os.remove('static/images/' + request.form['delete_one'])
            if request.form['delete_one'] in pic_label:
                label = pic_label[request.form['delete_one']]
                pic_label.pop(request.form['delete_one'])
                label_list_full.remove(label)
                # if (label not in label_list_full) and (label in label_list):
                #     # meaning if all the images in a certain classification have been deleted
                #     label_list.remove(label)  # when label is removed from label_list, the recipes are removed too
            return redirect('/')

        elif 'delete_all' in request.form:
            for del_file in os.listdir('static/images/'):
                os.remove('static/images/' + del_file)
            pic_label.clear()
            label_list_full.clear()
            # label_list.clear()
            return redirect('/')

        elif 'create_model' in request.form:
            apple_list = os.listdir('static/images')
            clf = load('apple_model.joblib')  # apple_model is a pre-trained model created from NN_Model
            for img_predict in apple_list:
                img_array = cv2.imread('static/images/' + img_predict)
                flat_img_array = cv2.resize(img_array, (50, 50))
                flat_img_array = flat_img_array.flatten()
                predict_apple = clf.predict([flat_img_array])
                predict_apple = predict_apple[0]  # brings prediction out of array
                print(predict_apple)
                predict_apple = apple_variety_translate[predict_apple]  # turns classification into actual variety
                print(predict_apple)
                pic_label.__setitem__(img_predict, predict_apple)  # adds the (image name, classification)
                label_list_full.append(predict_apple)
                # if predict_apple not in label_list:
                #     label_list.append(predict_apple)
                #     print(label_list)
            return redirect('/')

        else:
            files = request.files.getlist('filename')  # predict_file is the name
            for file in files:
                if file not in os.listdir('static/images/'):  # protects against adding multiple of same image
                    if file.filename != '':  # protects against error where you press submit without selecting an image
                        file.save(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(file.filename)))
                        # saves file into proper path
            return redirect('/')


if __name__ == '__main__':
    app.run()

# explanation for joblib --> created a model in NN_Model and saved it via 'apple_model.joblib'
# could load pre-trained model immediately --> saves a lot of time bc don't have to re-train each time
# if change model in the future be sure to run the file again so that it saves -->
