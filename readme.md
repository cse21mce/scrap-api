# Scraping-API

## Setup Locally

```bash
git clone https://github.com/cse21mce/scrap-api.git
```

## Package Installatoin

```bash
pip install -r requirment.txt
```

## Endpoints

Endpoint (/docs) for testing API and get an overview of Endpoints

## Usage

1. Endpoint (/scrape_all?start_date=[start_date]&end_date=[end_date]&ministry_id=[ministry_id]) -> http://127.0.0.1:8000/scrape_all?start_date=2024-08-24&end_date=2024-08-24&ministry_id=0'

---

---

```json
response: [
      {
    "title": "PM attends Conference of Governors at Rashtrapati Bhawan",
    "date_posted": "Posted On: 02 AUG 2024 2:06PM by PIB Delhi",
    "content": "The Prime Minister, Shri Narendra Modi attended the Conference of Governors presided by the President of India, Smt Droupadi Murmu at Rashtrapati Bhawan today. He remarked that it is an important forum for discussions on how Governors can foster development and serve society. The Prime Minister posted on X; “Attended the Conference of Governors this morning. This is an important forum in which we discussed how Governors can foster development and serve society.”   Attended the Conference of Governors this morning. This is an important forum in which we discussed how Governors can foster development and serve society. pic.twitter.com/asrrLB3vFQ   *** DS/TS",
    "ministry": "Prime Minister's Office",
    "images": null
  },
  {
    "title": "PM pays tributes to Pingali Venkayya on his birth anniversary",
    "date_posted": "Posted On: 02 AUG 2024 2:02PM by PIB Delhi",
    "content": "The Prime Minister, Shri Narendra Modi has paid tributes to Pingali Venkayya on his birth anniversary and remembered his efforts in giving the Tricolour to the nation. Shri Modi also urged the citizens to support the Har Ghar Tiranga movement by unfurling the Tricolour between 9th and 15th August and sharing their selfies on harghartiranga.com.  The Prime Minister posted on X: “Remembering Pingali Venkayya Ji on his birth anniversary. His effort in giving us the Tricolour will always be remembered.  Do support the Har Ghar Tiranga movement and unfurl the Tricolour between 9th and 15th August! Don’t forget to share your selfie on harghartiranga.com “   Remembering Pingali Venkayya Ji on his birth anniversary. His effort in giving us the Tricolour will always be remembered. Do support the #HarGharTiranga movement and unfurl the Tricolour between 9th and 15th August! Don’t forget to share your selfie on https://t.co/84MOUwgRyA   *** DS/TS",
    "ministry": "Prime Minister's Office",
    "images": null
  },
  {...},
  {...}
]
```

2. Endpoint (/scrape_single?url=[url]) -> http://127.0.0.1:8000/scrape_single?url=https://pib.gov.in/PressReleasePage.aspx?PRID=2040315

---

---

```json
response: {
  "title": "Signing of Donor Agreement between Ministry of Ayush, Government of India and WHO",
  "date_posted": "Posted On: 01 AUG 2024 5:40PM by PIB Delhi",
  "content": "The Ministry of Ayush, Government of India and the World Health Organization signed a Donor Agreement during a signing ceremony organized at WHO Headquarters in Geneva on 31st July, 2024. This agreement, which outlines the financial terms for implementing the activities of the WHO Global Traditional Medicine Centre (GTMC) in Jamnagar, Gujarat was signed by H.E Mr. Arindam Bagchi, Permanent Representative of India to the UN, Geneva and Dr. Bruce Aylward, Assistant Director-General for Universal Health Coverage and Life Course on behalf of Ministry of Ayush and WHO respectively. Vaidya Rajesh Kotecha, Secretary of Ayush, joined the event virtually. The event was moderated by Dr. Shyama Kuruvilla, Director a.i. of WHO GTMC and vote of thanks was delivered by Dr. Razia Pendse, Chef de Cabinet, representing the Director-General of WHO. Through this collaboration, the Government of the Republic of India will donate US$ 85 million over a period of 10 years (2022-2032) to support the operations of the WHO Global Traditional Medicine Centre (GTMC) in Jamnagar, Gujarat, India. The Donor agreement recognizes the establishment of the WHO Global Traditional Medicine Centre as a key knowledge hub for evidence-based Traditional Complementary and Integrative Medicine (TCIM) aiming to advance the health and well-being of people and the planet. With the approval of Union Cabinet; a Host Country Agreement was signed on 25th March, 2022 between Ministry of Ayush, Government of India and WHO, marking the establishment of WHO Global Traditional Medicine Centre in Jamnagar, Gujarat as the first and only global out-posted Centre (office) for traditional medicine across the globe. The interim office of the WHO-GTMC is already operational, working on developing capacity-building and training programs relevant to its objectives. These programs will include campus-based, residential or web-based training, in partnership with the WHO Academy and other strategic partners. The Ministry of Ayush has collaborated with WHO on various fronts, including the development of benchmark documents for training and practice in Ayurveda, Unani and Siddha systems, the creation of WHO terminology for these practices, the introduction of a second module in the Traditional Medicine Chapter of the International Classification of Diseases-11, the development of apps like M-Yoga and support for the International Pharmacopoeia of Herbal Medicine (IPHM). These collaborative efforts, including those involving the WHO GTMC, will help India in positioning traditional medicine on the global stage. The joint efforts of Ministry of Ayush, Government of India & WHO will not only benefit India but also contribute to the global health agenda, reinforcing our commitment to achieving the Sustainable Development Goals through Traditional Medicine. *** SK",
  "ministry": "AYUSH",
  "images": ["https://static.pib.gov.in/WriteReadData/userfiles/image/image001Z9KZ.jpg"]
}
```
