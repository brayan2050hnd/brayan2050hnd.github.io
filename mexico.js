    

  

    const loader = document.querySelector('.loader');

setTimeout(() => {
  loader.style.display = 'none';
}, 5000);

    
    
    
      const images1 = [
        "https://upload.wikimedia.org/wikipedia/commons/thumb/0/07/Canal_5_Honduras.webp/1200px-Canal_5_Honduras.webp.png",
        "https://i.ytimg.com/vi/2q1ltRgrtLk/hqdefault.jpg",
        "https://upload.wikimedia.org/wikipedia/commons/c/c3/Canal_5_HN_logo.png",
        "https://upload.wikimedia.org/wikipedia/commons/a/ad/Canal_5_HN_logo_2019.png",
      ];

      const images2 = [
        "https://upload.wikimedia.org/wikipedia/commons/f/ff/TSi_logo.png",
        "https://programacion.televicentro.com/images/tsi.png",
        "https://s3.amazonaws.com/prod-wp-tvc/wp-content/uploads/2020/05/Generica-TSi.png",
        "https://cdn.mitvstatic.com/programs/hn_noticiero-infantil-tsi_p_m.jpg"
      ];

      const images3 = [
        "https://upload.wikimedia.org/wikipedia/commons/4/40/Telecadena7y42018.png",
        "https://i.pinimg.com/originals/38/89/11/3889115d234269ff87bdcc812f815a6c.jpg",
        "https://s3.amazonaws.com/prod-wp-tvc/wp-content/uploads/2020/05/Generica-Canal-7.png",
        "https://programacion.televicentro.com/images/telecadena.png"
      ];
      
      
      
      
      const images4 = [
        "https://hch.tv/wp-content/uploads/2021/09/logos-hch-bueno-1.png",
        "https://www.televisiongratis.tv/components/com_televisiongratis/images/hch-en-vivo-889.jpg",
        "https://pbs.twimg.com/media/EPjyAw4XsAADHJc.jpg",
        "https://hch.tv/wp-content/uploads/2021/06/WhatsApp-Image-2021-06-13-at-5.54.02-PM.jpeg",
      ];

      const images5 = [
        "https://3dwarehouse.sketchup.com/warehouse/v1.0/content/public/52439c85-e2bd-4b9d-a51c-96a4fa0e51d1",
        "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRco0VV0bCbEa5pp7yJdwNhYOL-Wv0003SrpQ&usqp=CAU",
        "https://upload.wikimedia.org/wikipedia/commons/thumb/2/22/MetroTV_2000.svg/2560px-MetroTV_2000.svg.png",
        "https://w7.pngwing.com/pngs/859/451/png-transparent-metrotv-indonesia-television-channel-news-metro-city-television-text-trademark.png"
      ];

      const images6 = [
        "https://i0.wp.com/directostv.teleame.com/wp-content/uploads/2017/10/Canal-11-Aysen-en-vivo-Online.png?fit=1920%2C1080&ssl=1",
        "https://upload.wikimedia.org/wikipedia/commons/3/32/Canal_11_HN_logo_2010.png",
        "https://www.oncenoticias.hn/wp-content/uploads/2022/11/C11-1-990x557.jpg",
        "https://www.oncenoticias.hn/wp-content/uploads/2018/11/CANAL-11.jpg"
      ];
      
      
      const images7 = [
        "https://pbs.twimg.com/media/DM71p8GX0AENVWT.jpg:large",
        "https://apprecs.org/gp/images/app-icons/300/0c/com.yourappland.tdtv.jpg",
        "https://3dwarehouse.sketchup.com/warehouse/v1.0/content/public/898a3be8-230b-4b73-96db-a6163101384f",
        "https://lh3.googleusercontent.com/apXbKaSmEba3reAuL6Lcu3jXrh_BdfDxNU0fYUDRXHc1Q9OyQP8NH0-oER6VeURPjA=w1024"
      ];
      
      
      
      
      const images8 = [
        "https://i.ytimg.com/vi/dmOxCxMyJVs/hqdefault.jpg?sqp=-oaymwEjCPYBEIoBSFryq4qpAxUIARUAAAAAGAElAADIQj0AgKJDeAE=&rs=AOn4CLB3UEy-P_awVYXL9z4lKDdg-N1Qwg",
        "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQT_MfT5NRJ3kkOBG5MJmVr7v2LYKtFIYHyug&usqp=CAU",
        "https://2.bp.blogspot.com/--HxQ_rnA4hU/Wdv5wSG_xuI/AAAAAAAAAko/5vqniQKxFiYszx7QjEUjX4Sb3qQN-r7TQCLcBGAs//TEN-TV-Honduras.png",
        "https://www.tencanal10.tv/wp-content/uploads/2017/07/mintenani.jpg",
      ];

      const images9 = [
        "https://3dwarehouse.sketchup.com/warehouse/v1.0/content/public/67780b66-feb8-4d2d-909c-5661e68d4ec8",
        "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcR7EY4BFHsFaYKh0O6ZXXUeK1AeoJW3F8-W_A&usqp=CAU",
        "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRit-FZiN03VG1tIcchJof7p_SG6n42scxQXw&usqp=CAU",
        "https://yt3.googleusercontent.com/ytc/AL5GRJWlh6psUNchVdXl4Q9fCU3_v6HG7gppeHD8kHkJ=s900-c-k-c0x00ffffff-no-rj"
      ];

      
      
      
      
      const images10 = [
        "https://www.sitvhn.com/img/siTVlogo.png",
        "https://i.vimeocdn.com/portrait/33686991_640x640",
        "https://yt3.googleusercontent.com/uThTMNUcHcBv-LSYFhIQWMlrSStWeZfxeB97Iyfba_ay886x1jDd5rGRWl45F84Z7Go8v8G0=s900-c-k-c0x00ffffff-no-rj",
        "https://www.tradefairdates.com/logos/sitv_logo_1886.png"
      ];
      
      
      
      
      const images11 = [
        "https://upload.wikimedia.org/wikipedia/commons/thumb/2/26/VTV_HN_logo_2019.png/1200px-VTV_HN_logo_2019.png",
        "https://seeklogo.com/images/V/vtv-honduras-logo-3680BE9BFF-seeklogo.com.png",
        "https://3dwarehouse.sketchup.com/warehouse/v1.0/content/public/4efad423-b56b-42c9-b30b-12d49b8e146b",
        "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSoTgl7QnMFy6jNKem3ERB0wpyVy-GU6n6H3g&usqp=CAU",
      ];

      const images12 = [
        "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcR69DglBpa6QdwzsnwekxknXvFY01i2-fptcg&usqp=CAU",
        "https://upload.wikimedia.org/wikipedia/commons/2/2e/Cholusat_Sur_logo.png",
        "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQgfcIO9QfDfyIOKMsGZwIIZ7HEQvSgPaD_4g&usqp=CAU",
        "https://i.ytimg.com/vi/tFiDWaKUOzQ/maxresdefault.jpg"
      ];

      
      
      const images13 = [
        "https://chtv.hn/wp-content/uploads/2020/01/512-1.png",
        "https://is3-ssl.mzstatic.com/image/thumb/Purple125/v4/ac/3a/8f/ac3a8fee-f43b-b608-606c-d5895c438220/source/512x512bb.jpg",
        "https://3dwarehouse.sketchup.com/warehouse/v1.0/content/public/1f4385c1-69b0-4f58-b77c-47cc8d200c96",
        "https://i0.wp.com/chtv.hn/wp-content/uploads/2022/10/Screenshot_20221009-101913_Gallery.jpg?fit=1079%2C906&ssl=1"
      ];

      
      
      
      
      const images14 = [
        "https://3dwarehouse.sketchup.com/warehouse/v1.0/content/public/ede4742a-52b8-4717-a304-f850e4e09464",
        "https://pbs.twimg.com/media/CYuLvACWwAAq7hf.jpg",
        "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQgB2jNojHyYkSZoaefABfSPSfgDLNzcrF1FQ&usqp=CAU",
        "https://yt3.googleusercontent.com/ytc/AL5GRJXA7nqWA4doXqckVMI_kjs222pPhQzBw4E6pSIz=s900-c-k-c0x00ffffff-no-rj"
      ];
      
      
      
      
      const images15 = [
        "https://3dwarehouse.sketchup.com/warehouse/v1.0/content/public/38cead35-41aa-4c6f-8169-3ce42bdf432f",
        "https://www.teleprogreso.tv/wp-content/uploads/2019/09/logo-teleprogreso-header.jpg",
        "https://www.teleprogreso.tv/wp-content/uploads/2019/09/TP-senal-envivo.jpg",
        "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSY1HVGdl1Kz2oqDYTYhdP1-KHX7g7PdHcdhg&usqp=CAU",
      ];

      
      
      
      const images16 = [
        "https://3dwarehouse.sketchup.com/warehouse/v1.0/content/public/65e61197-9d99-4221-a7f7-6660f1af9283",
        "https://pbs.twimg.com/media/EU-VZcGUEAAHLmh.jpg",
        "https://image.winudf.com/v2/image/Y29tLmFydGljYS51bmV0dl9pY29uXzBfOTJjNzVmZDg/icon.png?w=&fakeurl=1 ",
        "https://cloudfront-us-east-1.images.arcpublishing.com/semana/CVLLEMMHPBHLZMPLFMQX46CTRA.jpg"
      ];

      
      
      
      
      const images17 = [
        "https://upload.wikimedia.org/wikipedia/commons/a/ac/Canal8hn2023.png",
        "https://upload.wikimedia.org/wikipedia/commons/2/2e/CANAL82022.png",
        "https://tnh.gob.hn/wp-content/uploads/2022/11/cropped-285512422_431662858967024_748898711325018620_n-e1667698342409.jpg",
        "https://directostv.teleame.com/wp-content/uploads/2018/03/TNH-%E2%80%93-Televisi%C3%B3n-Nacional-de-Honduras-en-vivo-Online.png"
      ];
      
      
      
      
      const images18 = [
        "https://play-lh.googleusercontent.com/yACFGtBzI_R0s-XY2r3wVTZW4VE4uMxNW2IkXAramPrckFmihjalpwvaFfhzu0SwRg0",
        "https://directostv.teleame.com/wp-content/uploads/2018/03/Alsacias-Canal-28-en-vivo-Online.png",
        "https://play-lh.googleusercontent.com/yACFGtBzI_R0s-XY2r3wVTZW4VE4uMxNW2IkXAramPrckFmihjalpwvaFfhzu0SwRg0",
        "https://yt3.googleusercontent.com/_Q2hUIr9zzEgvZV6sVCq3MAsImCBokujZGqbsL1W8rKIBE6pFYz0HGEdhEvuXl3GXvZe7TP63w=s900-c-k-c0x00ffffff-no-rj",
      ];

      
      
      
      
      
      
  const images19 = [
        "https://media.sipiapa.org/adjuntos/185/imagenes/001/797/0001797630.jpg",
        "https://www.coolstreaming.us/img/ch/ima10097052250.jpg",
        "https://signisalc.org/wp-content/uploads/2021/04/TV-GLOBO.png-S.png",
        "https://livetvcentral.com/imgs/tvs/3915.jpg"
      ];

      
      
      
      
      const images20 = [
        "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSIhlY2S4wKNuOMgmfu72M7nutxAYZrPntLFQ&usqp=CAU",
        "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcR2undiCdzuBIHZXDKU6WyAiWLR7V9SkoH95w&usqp=CAU",
        "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSIhlY2S4wKNuOMgmfu72M7nutxAYZrPntLFQ&usqp=CAU",
        "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcR2undiCdzuBIHZXDKU6WyAiWLR7V9SkoH95w&usqp=CAU"
      ];
      
      
      
      
      const images21 = [
        "https://campustv.utalca.cl/wp-content/uploads/2019/01/Avatar-CampusTV-1-800x450.png",
        "https://upload.wikimedia.org/wikipedia/commons/8/8a/CampusTv_logo.png",
        "https://cdn.domestika.org/c_fill,dpr_1.0,f_auto,h_1200,pg_1,t_base_params,w_1200/v1591118094/project-covers/000/743/712/743712-original.png?1591118094",
        "https://www.campustv-b2b.info/campustv/img/campustv_logo_333x185.png",
      ];

      
      
      
      
      const images22 = [
        "https://yt3.googleusercontent.com/ytc/AL5GRJX2vDJIntB5-CcLgzasMpRWUexIp8jKDgPEk4i8ZQ=s900-c-k-c0x00ffffff-no-rj",
        "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTnEjfEG0bSMXfMdSXQGwrkWc8jb6G1iXrPlQ&usqp=CAU",
        "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTQW2C-9-K3ZV0sc9syXzCJeif_BuNkgLUZIQ&usqp=CAU",
        "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQXHX20i1RRm-5CLPbbtjgCZOyRNKhLJbSUpw&usqp=CAU"
      ];

      
      
      
      
      const images23 = [
        "https://3dwarehouse.sketchup.com/warehouse/v1.0/content/public/85626917-65c9-4199-9a9c-7b9399686e1d",
        "https://2.bp.blogspot.com/-Rel6fLKrEck/W9Rju1-dw8I/AAAAAAAADy8/r09pI06pquMRFYposBGBrSiHGUqEFqtbgCPcBGAYYCw/w1200-h630-p-k-no-nu/suyapa.jpg",
        "https://3dwarehouse.sketchup.com/warehouse/v1.0/content/public/4ea9550c-cda7-4189-9949-435df916f90c",
        "https://directostv.teleame.com/wp-content/uploads/2018/03/suyapa-tv.png"
      ];
      
      
      
      
      const images24 = [
        "https://directostv.teleame.com/wp-content/uploads/2018/03/tvcris.png",
        "https://sites.google.com/site/ebenezerencolombia/_/rsrc/1472875828664/home/487648_421821841201548_261784240_n.jpg?height=673&width=457",
        "https://i.pinimg.com/236x/37/50/d4/3750d4c19794627ffab6db72aff47381--logos-style.jpg",
        "https://ebenezer.hn/themes/ebenehon/assets/img/ot-img/logo-blue.png",
      ];

      
      
      
      
      const images25 = [
        "https://guayapetv.hn/img/img1.png",
        "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTk9ZUn3g83Oy6Ra4HTXoTBFcKXUizBq8jEcg&usqp=CAU",
        "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRAEYbcVgLg8gr8AAkSLxmn2TlZOEGTraG3IA&usqp=CAU",
        "https://static.wixstatic.com/media/ead229_3a39ec0cfa9248219ed0f4eb2b48a3f7~mv2.png/v1/fill/w_529,h_159,al_c,q_85,usm_0.66_1.00_0.01,enc_auto/ead229_3a39ec0cfa9248219ed0f4eb2b48a3f7~mv2.png"
      ];

      
      
      
      
      const images26 = [
        "https://image.roku.com/developer_channels/prod/b0564acdb9c67295acae4e5cf3978ed35795180f9728f21080885a8733d124cd.png",
        "https://www.diosteve.org/wp-content/uploads/2022/04/LOGO-200x200.png",
        "https://www.diosteve.org/wp-content/uploads/2022/04/Radio-Dios-Te-Ve-3-1.png",
        "https://pbs.twimg.com/profile_images/886623373614342144/TkVOFEox_400x400.jpg"
      ];
      
      
      
      
      const images27 = [
        "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSUdiTNPJY2s-0DWiubgyDo2Gchw8dMYC9z5A&usqp=CAU",
        "https://d3ld16hid784z2.cloudfront.net/media/2020/03/cacncan.png",
        "https://d3ld16hid784z2.cloudfront.net/media/2020/02/logo-ltv-1.png",
        "https://yt3.googleusercontent.com/R-r_kmKCoJ32HyCF1NDodPVA7OWmQiJd-yX7vggwb83z-Xi1CjQpOXHnkcv0Ml82tHeu-rIaFpY=s900-c-k-c0x00ffffff-no-rj",
      ];

      
          
      
      
      
      
      const images28 = [
        "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRhV82JeYtZnT-eLAraiF7MsDpaPP8gxHSp8A&usqp=CAU",
        "https://lh3.googleusercontent.com/s2yCmMBUZsOFNtN000ldPOKW9YSK70Fbkq_JeyLyczvNHAfT-KBe86fzOG6CuoSIn8M=s150-rw",
        "https://1.bp.blogspot.com/-71JpI8dJtFI/XRy7_64nZ7I/AAAAAAAAH7E/G2XCzJ3_XAsv8A-KTdynl-GIoOXIY-28QCLcBGAs/w1200-h630-p-k-no-nu/TeleDanli%2BCanal%2B9.png",
        "https://yt3.googleusercontent.com/ytc/AGIKgqMAEuNdBP3euuXZrkcqVb2oo1bPQ7bjhJj9TwU1=s900-c-k-c0x00ffffff-no-rj"
      ];

      
      
      
      
      const images29 = [
        "https://static.vecteezy.com/system/resources/previews/009/124/772/original/jbn-logo-jbn-letter-jbn-letter-logo-design-initials-jbn-logo-linked-with-circle-and-uppercase-monogram-logo-jbn-typography-for-technology-business-and-real-estate-brand-vector.jpg",
        "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcS9dVkXwxLMTMjLI4yxz_ubePjk2yj0aEqGyQ&usqp=CAU",
        "https://jbn39.com/wp-content/uploads/2019/02/logo-01-1.png",
        "https://1.bp.blogspot.com/-AaOnbW59snM/XRy3KgUXkuI/AAAAAAAAH64/BCWjPP1McoEHsOwYZMXJP8QFPQzd-wzEACLcBGAs/s1600/Canal%2BJBN.png"
      ];
      
      
      
      
      const images30 = [
        "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSUdiTNPJY2s-0DWiubgyDo2Gchw8dMYC9z5A&usqp=CAU",
        "https://d3ld16hid784z2.cloudfront.net/media/2020/03/cacncan.png",
        "https://d3ld16hid784z2.cloudfront.net/media/2020/02/logo-ltv-1.png",
        "https://yt3.googleusercontent.com/R-r_kmKCoJ32HyCF1NDodPVA7OWmQiJd-yX7vggwb83z-Xi1CjQpOXHnkcv0Ml82tHeu-rIaFpY=s900-c-k-c0x00ffffff-no-rj",
      ];

      
      
          
      

      const imgElements = document.querySelectorAll(".card-img");

      let index1 = 0;
      let index2 = 0;
      let index3 = 0;
      let index4 = 0;
      let index5 = 0;
      let index6 = 0;
      let index7 = 0;
      let index8 = 0;
      let index9 = 0;
      let index10 = 0;
      let index11 = 0;
      let index12 = 0;
      let index13 = 0;
      let index14 = 0;
      let index15 = 0;
      let index16 = 0;
      let index17 = 0;
      let index18 = 0;
      let index19 = 0;
      let index20 = 0;
      let index21 = 0;
      let index22 = 0;
      let index23 = 0;
      let index24 = 0;
      let index25 = 0;
      let index26 = 0;
      let index27 = 0;
      let index28 = 0;
      let index29 = 0;
      let index30 = 0;
      
      
      
      
      
      
      
      setInterval(() => {
        index1 = (index1 + 1) % images1.length;
        imgElements[0].src = images1[index1];
      }, 4000);

      setInterval(() => {
        index2 = (index2 + 1) % images2.length;
        imgElements[1].src = images2[index2];
      }, 4500);

      setInterval(() => {
        index3 = (index3 + 1) % images3.length;
        imgElements[2].src = images3[index3];
      }, 5000);
    
    
    setInterval(() => {
        index4 = (index4 + 1) % images1.length;
        imgElements[3].src = images4[index4];
      }, 5500);

      setInterval(() => {
        index5 = (index5 + 1) % images2.length;
        imgElements[4].src = images5[index5];
      }, 6000);

      setInterval(() => {
        index6 = (index6 + 1) % images3.length;
        imgElements[5].src = images6[index6];
      }, 6500);
    
    
    setInterval(() => {
        index7 = (index7 + 1) % images1.length;
        imgElements[6].src = images7[index7];
      }, 7000);
    
    setInterval(() => {
        index8 = (index8 + 1) % images2.length;
        imgElements[7].src = images8[index8];
      }, 7500);
    
    setInterval(() => {
        index9 = (index9 + 1) % images3.length;
        imgElements[8].src = images9[index9];
      }, 8000);
    
    
    
      
    
    setInterval(() => {
      index10 = (index10 + 1) % images1.length;
        imgElements[9].src = images10[index10];
      }, 8500);
    
    setInterval(() => {
    index11 = (index11 + 1) % images2.length;
       imgElements[10].src = images11[index11];
      }, 9000);
    
    setInterval(() => {
     index12 = (index12 + 1) % images3.length;
       imgElements[11].src = images12[index12];
      }, 9500);
    
    
    
    
    
    
    
    setInterval(() => {
      index13 = (index13 + 1) % images1.length;        imgElements[12].src = images13[index13];
      }, 10000);
    
    setInterval(() => {
    index14 = (index14 + 1) % images2.length;
       imgElements[13].src = images14[index14];
      }, 10500);
    
    setInterval(() => {
     index15 = (index15 + 1) % images3.length;
       imgElements[14].src = images15[index15];
      }, 11000);
    
    
    
    
    
    
    
    setInterval(() => {
      index16 = (index16 + 1) % images1.length;        imgElements[15].src = images16[index16];
      }, 11500);
    
    setInterval(() => {
    index17 = (index17 + 1) % images2.length;
       imgElements[16].src = images17[index17];
      }, 12000);
    
    setInterval(() => {
     index18 = (index18 + 1) % images3.length;
       imgElements[17].src = images18[index18];
      }, 12500);
    
    
    
    
    
    setInterval(() => {
      index19 = (index19 + 1) % images1.length;        imgElements[18].src = images19[index19];
      }, 4000);
    
    setInterval(() => {
    index20 = (index20 + 1) % images2.length;
       imgElements[19].src = images20[index20];
      }, 4500);
    
    setInterval(() => {
     index21 = (index21 + 1) % images3.length;
       imgElements[20].src = images21[index21];
      }, 5000);
    
    
    
    
    
    
    setInterval(() => {
      index22 = (index22 + 1) % images1.length;        imgElements[21].src = images22[index22];
      }, 5500);
    
    setInterval(() => {
    index23 = (index23 + 1) % images2.length;
       imgElements[22].src = images23[index23];
      }, 6000);
    
    setInterval(() => {
     index24 = (index24 + 1) % images3.length;
       imgElements[23].src = images24[index24];
      }, 6500);
    
    
    
    
    
    
    setInterval(() => {
      index25 = (index25 + 1) % images1.length;        imgElements[24].src = images25[index25];
      }, 7000);
    
    setInterval(() => {
    index26 = (index26 + 1) % images2.length;
       imgElements[25].src = images26[index26];
      }, 7500);
    
    setInterval(() => {
     index27 = (index27 + 1) % images3.length;
       imgElements[26].src = images27[index27];
      }, 8000);
    
    
    
    
    
    
    
    setInterval(() => {
     index28 = (index28 + 1) % images1.length;       
       imgElements[27].src = images28[index28];
      }, 8500);
    
    
    setInterval(() => {
    index29 = (index29 + 1) % images2.length;
       imgElements[28].src = images29[index29];
      }, 9000);
    
    setInterval(() => {
     index30 = (index30 + 1) % images3.length;
       imgElements[29].src = images30[index30];
      }, 9500);
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    var contenedor = document.getElementById('contenedor');

function reproducirContenido(tipo, url) {
	// Vaciamos el contenido del contenedor
	contenedor.innerHTML = '';

	// Creamos el elemento correspondiente según el tipo de contenido
	if (tipo === 'iframe') {
		var iframe = document.createElement('iframe');
		iframe.setAttribute('src', url);
		iframe.setAttribute('frameborder', '0');
		iframe.setAttribute('allowfullscreen', 'true');
		iframe.setAttribute('width', '100%');
		iframe.setAttribute('height', '200em');
		contenedor.appendChild(iframe);
	} else if (tipo === 'm3u8') {
		var video = document.createElement('video');
		video.setAttribute('controls', '');
		
		var source = document.createElement('source');
		source.setAttribute('src', url);
		source.setAttribute('type', 'application/x-mpegURL');
		

		
		video.setAttribute('width', '100%');
  video.setAttribute('height', '100%');
  
		video.appendChild(source);
		contenedor.appendChild(video);
	}
}











const nav = document.querySelector("#nav");
const abrir = document.querySelector("#abrir");
const cerrar = document.querySelector("#cerrar");

abrir.addEventListener("click", () => {
    nav.classList.add("visible");
})

cerrar.addEventListener("click", () => {
    nav.classList.remove("visible");
})






document.getElementById("myBtn").addEventListener("click", function(){
   location.reload();
});








function searchImagesAndButtons() {
  const term = document.getElementById('search').value.toLowerCase();
  
  // Ocultar todos los elementos h4
  const h2 = document.getElementsByTagName('h2');
  for (let i = 0; i < h2.length; i++) {
    h2[i].style.display = 'none';
  }
  
  
  
  
    const h1 = document.getElementsByTagName('h1');
  for (let i = 0; i < h1.length; i++) {
    h1[i].style.display = 'none';
  }
  
  
  
  const images = document.getElementsByTagName('img');
  
  const buttons = document.getElementsByTagName('button');
  
  for (let i = 0; i < images.length; i++) {
    const alt = images[i].alt.toLowerCase();
    if (alt.includes(term)) {
      images[i].style.display = 'block';
    } else {
      images[i].style.display = 'none';
    }
  }
  
  for (let i = 0; i < buttons.length; i++) {
    const text = buttons[i].textContent.toLowerCase();
    if (text.includes(term)) {
      buttons[i].style.display = 'block';
    } else {
      buttons[i].style.display = 'none';
    }
  }
}







  