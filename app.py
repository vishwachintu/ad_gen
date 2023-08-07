import streamlit as st
import openai
import random
import pandas as pd
from csv import writer
from csv import DictWriter
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw 


st.title("Ad cre'AI'tor")


# product info
product_prompt = st.text_input("enter product info")
# name of the product
product_name_prompt = st.text_input("enter product name")
# audience selection
audience_prompt = st.selectbox(
    "Create audience",
    ["Child", "Young Adults", "Middle-aged Adults", "Old-aged Adults"],
    help="""Choose the input info of your audience""",
)
# features of the product
features_prompt = st.text_area(
    "enter product features", help="""enter product information by comma seperating"""
)

# api key
openai.api_key = "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" # enter your api key here


def add_creator():
    indentation_op = []
    tagline_list = []
    for _ in range(2):
        response = openai.Completion.create(
            model="text-davinci-003",
            # prompt=f"Write a creative ad for the following product to run \
            #     on Facebook,instagram aimed at {audience_prompt}:\n\
            # \nProduct: product features were{product_prompt} with product name {product_name_prompt} \
            # {features_prompt}",
            prompt = f"For the following product {product_name_prompt}, \
             create an advertisement to run on Facebook and Instagram with a focus on {audience_prompt}. \
                Product: {product_name_prompt} product qualities were {product_prompt} with the product name {product_name_prompt}",
            temperature=0.5,
            max_tokens=100,
            top_p=1.0,
            frequency_penalty=0.0,
            presence_penalty=0.0,
        )
        tagline_respone = openai.Completion.create(
            model="text-davinci-003",
            # prompt=f"write a tagline with {product_prompt, product_name_prompt} ",
            prompt=f"write a tagline for {product_name_prompt} with following information {product_prompt} ",
            temperature=0.5,
            max_tokens=256,
            top_p=1,
            best_of=1,
            frequency_penalty=0,
            presence_penalty=0,
        )
        indentation_op.append(response["choices"][0]["text"])
        tagline_list.append(tagline_respone["choices"][0]["text"])
    return indentation_op, tagline_list

with st.container():
    if st.button("Generate ad"):
        output_generations = add_creator()

        st.write("Taglines:")
        st.write(output_generations[1])
        st.write("Ads:")
        st.write(output_generations[0])


        # image
        # def write_text_on_images(img, text):
        #     final_res = []
        #     draw = ImageDraw.Draw(img)
        #     font = ImageFont.truetype("arial.ttf", 20)  # load font
        #     W,H = img.size
        #     _, _, w, h = draw.textbbox((0, 0), text, font=font)
        #     new_width = (W - w) / 2
        #     new_height = (H - h) / 2
        #     final_result = draw.text((new_width,new_height), text.strip('"'), font=font, fill=(113, 166, 210)) #(200, 200, 0)
        #     final_res.append(final_result)
        #     return final_res
        
        img1_bg = Image.open("bg_img.jpeg")
        text_1 =  output_generations[1][0]
        draw = ImageDraw.Draw(img1_bg)
        font = ImageFont.truetype("arial.ttf", 25)  # load font
        W,H = img1_bg.size
        _, _, w, h = draw.textbbox((0, 0), text_1, font=font)
        new_width = (W - w) / 2
        new_height = (H - h) / 2
        draw.text((new_width,new_height), text_1.strip('"'), font=font, fill=(113, 166, 210)) #(200, 200, 0)

        # img_1= write_text_on_images(img1_bg, text_1)

        img2_bg = Image.open("img_2.jpeg")
        W2,H2 = img2_bg.size
        text_2 =  output_generations[1][1]
        draw2 = ImageDraw.Draw(img2_bg)
        font2 = ImageFont.truetype("arial.ttf", 25)  # load font
        _, _, w2, h2 = draw2.textbbox((0, 0), text_2, font=font)
        new_width2 = (W2 - w2) / 2
        new_height2 = (H2 - h2) / 2
        draw2.text((new_width2,new_height2), text_2.strip('"'), font=font2, fill=(0, 0, 0)) #(200, 200, 0)

        st.image([img1_bg,img2_bg], caption=["Template images for taglines_1","Template images for taglines_2"])

        generation_dict = {
            "ProductInfo": product_prompt,
            "ProductName": product_name_prompt,
            "Audience": audience_prompt,
            "Features": features_prompt,
            "Generations": output_generations[1],
            "Tagline": output_generations[0],
        }

        field_names = [
            "ProductInfo",
            "ProductName",
            "Audience",
            "Features",
            "Generations",
            "Tagline",
        ]
        # Create a file object for this file
        with open("event.csv", "a") as f_object:
            # You will get a object of DictWriter
            dictwriter_object = DictWriter(f_object, fieldnames=field_names)

            # Pass the dictionary as an argument to the Writerow()
            dictwriter_object.writerow(generation_dict)

            # Close the file object
            f_object.close()

        # Add a next button and a previous button
        # page_number = 0
        # last_page = 10

        # prev, _ ,next = st.columns([1, 10, 1])

        # if next.button("Next"):

        #     if page_number + 1 > last_page:
        #         page_number = 0
        #     else:
        #         page_number += 1

        # if prev.button("Previous"):

        #     if page_number - 1 < 0:
        #         page_number = last_page
        #     else:
        #         page_number -= 1

        # # Get start and end indices of the next page of the dataframe

        # # Index into the sub dataframe
        # # Get start and end indices of the next page of the dataframe
        # start_idx = page_number
        # end_idx = (1 + page_number)

        # sub_df = add_creator()[start_idx:end_idx]
        # st.write(sub_df)