#!/usr/bin/python
# -*- coding:utf-8 -*-
import sys
import os
picdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'pic')
libdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'lib')
if os.path.exists(libdir):
    sys.path.append(libdir)

import logging
from waveshare_epd import epd1in02
import time
from PIL import Image, ImageDraw, ImageFont
import traceback

logging.basicConfig(level=logging.DEBUG)

try:
    logging.info("epd1in02 Demo")
    
    epd = epd1in02.EPD()
    logging.info("init and Clear")
    epd.Init()
    epd.Clear()
    
    # Set up the font (Courier-like font)
    font = ImageFont.truetype(os.path.join(picdir, 'tom-thumb.ttf'), 6)

    # Partial update
    logging.info("4.show numbers...")
    epd.Partial_Init()    

    number_image = Image.new('1', (epd.width, epd.height), 255)
    number_draw = ImageDraw.Draw(number_image)
    
    image_old = epd.getbuffer(number_image)
    y_position = epd.height - 8  # Start position at the bottom of the screen

    # Your letter, split into lines
    text_options = {
        "0": [
            "January 15, 2006",
            "",
            "Your honor,",
            "",
            "The central factual/legal",
            "question is whether or not",
            "Mr. Johnson's firm, as the",
            "successor plaintiff's attorney,",
            "ever acknowledged the lien of",
            "LawInc when it took over",
            "the file from the original",
            "plaintiff's attorney by",
            "substitution of counsel.",
            "",
            "It appears that no writing",
            "was ever signed by Mr. Johnson's",
            "firm and delivered to LawInc,",
            "and thus we need to focus on",
            "the legal effect of substitution",
            "and or any other internal writings",
            "of Mr. Johnson and his firm",
            "which would tend to acknowledge",
            "that the lien of LawInc",
            "did exist when it got",
            "the file and that",
            "it would be honored.",
            "",
            "Please call me upon your",
            "receipt of these papers",
            "to discuss this matter.",
            "",
            "Very truly yours,",
            "MTS, Esq."
            "",
            "",
            "MTS:js"
        ],
        "1": [
            "State of New York",
            "Department of State",
            "",
            "Certificate of Assumed Name",
            "",
            "1. The entity type is:",
            "Corporation",
            "",
            "2. The exact name of the",
            "entity as registered is:",
            "A-Z Drugs, Inc.",
            "",
            "3. The county within this",
            "state in which the office",
            "of the entity is located is:",
            "Kings",
            "",
            "4. The date of filing of the",
            "original certificate of",
            "incorporation with the",
            "Department of State is:",
            "January 1, 1997",
            "",
            "5. The entity is authorized to",
            "do business in New York State.",
            "",
            "6. The Assumed Name the",
            "corporation will use is:",
            "XLNT Pharmacy",
            "",
            "7. The principal place of",
            "business under the assumed name",
            "is 810 Fifth Ave, Brooklyn",
            "",
            "This certificate is executed",
            "under the penalties of perjury.",
            "",
            "Notary Public:",
            "- Andrew Smith, Esq.",
            "- Commission Expires: 2/11/25",
            "",
            "End of Certificate"
        ],
        "2": [
            "March 10, 2007",
            "",
            "Re: Survey",
            "",
            "Dear Mr. Jones,",
            "",
            "Thank you for yours of",
            "March 7, 2007.",
            "",
            "Please note that the",
            "conditions identified in",
            "your letter as described",
            "on the survey inspection were",
            "in existence according to",
            "Seller on the date he took",
            "occupancy of the premises",
            "in or about 1991.",
            "",
            "Additionally, according to",
            "Seller, the conditions had",
            "existed since about the 1930s",
            "according to his grantor,",
            "now deceased.",
            "",
            "According to the contract rider,",
            "paragraph D, since Seller",
            "is not able to deliver title",
            "free of these particular",
            "objections and is not required",
            "to bring any action or",
            "proceeding or otherwise incur",
            "any expense to render the",
            "title to the premises marketable,",
            "kindly advise whether your",
            "client intends to go forward",
            "with the purchase subject to",
            "these survey issues or desires",
            "a refund of your down payment",
            "in this matter.",
            "",
            "Thank you for your",
            "attention to this letter.",
            "",
            "Very truly yours,",
            "MTS, Esq."
            "",
            "",
            "MTS:js"
        ],
        "3": [
            "Satisfaction of Lien",
            "",
            "Know All Men By These Presents,",
            "that the Mechanics Lien filed in",
            "the office of the County Clerk",
            "of the County of Kings on the",
            "11th of January, 2006, in favor",
            "of a claim against a building in",
            "lack of an approval situated on",
            "the westerly side of 9th Avenue,",
            "25 feet and 2 inches southerly",
            "of 16th Street, being 100 feet",
            "and 0 inches wide, front and rear",
            "by 25 feet and 0 inches deep on",
            "each side, and known as number",
            "1606 9th Avenue, Brooklyn,",
            "New York, block 707, lots 37 and 38,",
            "for the sum of $2,876.30, is",
            "hereby acknowledged to be",
            "fully paid and satisfied.",
            "",
            "And the undersigned hereby",
            "directs that said Mechanics Lien",
            "be discharged of record.",
            "",
            "Signed:",
            "MTS, Esq.",
            "",
            "Acknowledged before me this",
            "27th of April, 2008",
            "",
            "Notary Public:",
            "Andrew Smith, Esq.",
            "Commission Expires: 2/11/25"
        ]
    }

    # Default text_lines
    text_lines = text_options.get("1")

    # Capture command line argument for letter option
    if len(sys.argv) > 1:
        letter_option = sys.argv[1]
        text_lines = text_options.get(letter_option, text_lines)  # Use default if option not found

    for line in text_lines:

        # Shift the existing content up by 20 pixels
        shifted_image = number_image.crop((0, 8, epd.width, epd.height))
        number_image.paste(shifted_image, (0, 0))
        number_draw.rectangle((0, epd.height - 8, epd.width, epd.height), fill=255)  # Clear the bottom line space
    
        # Draw the new line at the bottom
        number_draw.text((2, epd.height - 8), line, font=font, fill=0)
    
        # Rotate the image by 270 degrees
        rotated_image = number_image.rotate(270, expand=True)
    
        # Display the new line and update the old image buffer
        epd.DisplayPartial(image_old, epd.getbuffer(rotated_image))
        image_old = epd.getbuffer(rotated_image)

        # Pause for 1 second
        time.sleep(1.5)

        y_position -= 8  # Move up for the next line
    
        # Break if we've reached the bottom of the screen
        if y_position + 8 > epd.height:
            break

    logging.info("Completed displaying numbers")

    logging.info("Clear...")
#     epd.Init()
#     epd.Clear()
    
    logging.info("Goto Sleep...")
    epd.Sleep()
        
except IOError as e:
    logging.info(e)
    
except KeyboardInterrupt:    
    logging.info("ctrl + c:")
    epd1in02.epdconfig.module_exit()
    exit()