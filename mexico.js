    

  

    const loader = document.querySelector('.loader');

setTimeout(() => {
  loader.style.display = 'none';
}, 5000);

    
    
    
      const images1 = [
        "https://3dwarehouse.sketchup.com/warehouse/v1.0/content/public/52d0ed62-2a8a-4059-9a21-ee2a04989dc4",
        "https://upload.wikimedia.org/wikipedia/commons/thumb/2/2e/Canal_5_2016.svg/1200px-Canal_5_2016.svg.png",
        "https://3dwarehouse.sketchup.com/warehouse/v1.0/content/public/2de3b364-097e-45ce-addf-2835e1b129ec",
        "https://upload.wikimedia.org/wikipedia/commons/0/07/Logotipo-Canal-5-M%C3%A9xico.png",
      ];

      const images2 = [
        "https://3dwarehouse.sketchup.com/warehouse/v1.0/content/public/870a8ff9-2af0-4ab9-9b85-45ddbefd6c5c",
        "https://wpdicta-ha-staticfiles-media-v1.s3.amazonaws.com/wp-content/uploads/2019/09/01051030/estrellas.jpg",
        "https://televisa.brightspotcdn.com/dims4/default/41ae5f7/2147483647/strip/true/crop/980x551+0+101/resize/1200x675!/quality/90/?url=https%3A%2F%2Ftelevisa-brightspot.s3.amazonaws.com%2Fapi%2Fhttp%3A%2F%2Fi.lasestrellas.tv%2F2016%2F08%2Festrellas-logo.png",
        "https://upload.wikimedia.org/wikipedia/commons/thumb/8/85/Canal_de_las_Estrellas_logo.svg/1200px-Canal_de_las_Estrellas_logo.svg.png"
      ];

      const images3 = [
        "https://www.luciernagainformativa.com/wp-content/uploads/2020/05/comedia.jpg",
        "https://selectra.mx/sites/selectra.mx/files/styles/_default/public/images/distrito-comedia-825x293.png",
        "https://upload.wikimedia.org/wikipedia/commons/6/6b/DistritoComediaLOGO2018.png",
        "https://upload.wikimedia.org/wikipedia/commons/0/09/Logo_Distrito_Comedia.png"
      ];
      
      
      
      
      const images4 = [
        "https://isopixel.net/wp-content/uploads/2007/08/tlnovelas-logo.png",
        "https://images.squarespace-cdn.com/content/v1/5bb2ffa57a1fbd5c3246777a/1551724487451-Y4K4B6ICD41GQY406EAN/tlnovelas_main.jpg?format=1000w",
        "https://lh3.googleusercontent.com/t3ZFO8Bld254mHxRozAsjdUxVZeyqLiFRv_Qw2MAVFq1gp6pi7s9s0UowU6RYeq2FdRay7SheLbV61DxJF4NsItebx130N2dFym8wyAK2BED8fQiLGvSaWshSTo9-dc0k5QeMcr5GQ=w1920-h1080",
        "https://upload.wikimedia.org/wikipedia/commons/thumb/b/bd/Tlnovelas_2011_logo.svg/2560px-Tlnovelas_2011_logo.svg.png",
      ];

      const images5 = [
        "https://pbs.twimg.com/media/FPG30FjUYAEtpAF.jpg",
        "https://www.fibratvchihuahua.com.mx/media/uploads/web/guia/b113_-_ADN_40_2019-10-22_231420.124868badn40_Mesa_de_trabajo_1.png",
        "https://tvazteca.brightspotcdn.com/dims4/default/8beff58/2147483647/strip/true/crop/1280x720+0+0/resize/968x545!/format/jpg/quality/80/?url=http%3A%2F%2Ftv-azteca-brightspot.s3.amazonaws.com%2Fba%2F74%2Fb9733bb75b83f2e1e92ce8c1f3c7%2F0",
        "https://tvazteca.brightspotcdn.com/58/74/8f13538947b7a5e8a0c8989612e1/adn-40-512x512-color-02.png"
      ];

      const images6 = [
        "https://i0.wp.com/directostv.teleame.com/wp-content/uploads/2019/11/Ingenio-TV-en-vivo-Online.png?resize=696%2C392&ssl=1",
        "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcR0r92X4s6tH8NFfrLPjN-64ym_-s5_XNW-bg&usqp=CAU",
        "https://directostv.teleame.com/wp-content/uploads/2019/11/Aprende-TV-en-vivo-Online.png",
        "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTCmUeNZZqTocUwWy3P4R0TOTE0eSMqOKVfBw&usqp=CAU"
      ];
      
      
      const images7 = [
        "https://i.ytimg.com/vi/TzrXpBu660A/maxresdefault.jpg",
        "https://i.ytimg.com/vi/gQ11ILNEvq8/maxresdefault.jpg",
        "https://www.radioformula.com.mx/u/fotografias/m/2022/2/3/f1280x720-318653_450328_5050.jpg",
        "https://i.ytimg.com/vi/5GMxj6RnKq4/maxresdefault.jpg"
      ];
      
      
      
      
      const images8 = [
        "https://upload.wikimedia.org/wikipedia/commons/5/5e/Multimedios_Television.png",
        "https://i.ytimg.com/vi/UckJTnjZI5k/maxresdefault.jpg",
        "https://i.ytimg.com/vi/iaPUCNAvpTE/maxresdefault.jpg",
        "https://i.pinimg.com/736x/36/ae/a4/36aea42445a7f4fb199b8c34c9ac55f5.jpg",
      ];

      const images9 = [
        "https://directostv.teleame.com/wp-content/uploads/2018/06/Canal-7-Salta-en-vivo-Online.png",
        "https://directostv.teleame.com/wp-content/uploads/2019/11/Canal-7-SLP-en-vivo-Online-1.png",
        "https://cc.org.mx/wp-content/uploads/2021/03/Canal7-570x570.png",
        "https://canal7slp.tv/2020/wp-content/uploads/2019/05/logo-250.jpg"
      ];

      
      
      
      
      const images10 = [
        "https://upload.wikimedia.org/wikipedia/commons/thumb/a/a3/Logo_canal_13_XHDF_1991-1993.svg/2560px-Logo_canal_13_XHDF_1991-1993.svg.png",
        "https://w7.pngwing.com/pngs/429/682/png-transparent-logo-mexico-city-imevision-tv-azteca-azteca-uno-1974-purple-text-trademark.png",
        "https://upload.wikimedia.org/wikipedia/commons/thumb/1/16/Logo_Canal_13_Imevision_1974-1985.svg/995px-Logo_Canal_13_Imevision_1974-1985.svg.png",
        "https://www.canal13ventas.com/wp-content/uploads/2022/06/cropped-c13mini.png"
      ];
      
      
      
      
      const images11 = [
        "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcS-eQDBOlp2zMU0UFA7-NXxyisVrsXug1R1GA&usqp=CAU",
        "https://directostv.teleame.com/wp-content/uploads/2017/10/Canal-28-Chihuahua-en-vivo-Online.png",
        "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcS0XYfl3UXXLS_UY7_IQ03Tv1OHY8Tr1ZeBVg&usqp=CAU",
        "https://yt3.googleusercontent.com/ytc/AGIKgqMFv8qoZFhb097bYU1IfYodP_cX-hOLSSNBHN6_=s900-c-k-c0x00ffffff-no-rj",
      ];

      const images12 = [
        "https://www.canalcatorce.tv/descargas/logo_descargas.jpg",
        "https://upload.wikimedia.org/wikipedia/commons/thumb/0/01/Logo_Canal_14_M%C3%A9xico.svg/1200px-Logo_Canal_14_M%C3%A9xico.svg.png",
        "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQrF3LGPGE4D0PAbyFTw8GdEPuIIYUueD30QA&usqp=CAU",
        "https://i.ytimg.com/vi/bVvuvVLOXu8/maxresdefault.jpg"
      ];

      
      
      const images13 = [
        "https://www.canaldelcongreso.gob.mx/assets/img/logo.jpg",
        "https://www.canaldelcongreso.gob.mx/Resources/Medias/Streaming/1m0qf1v4.png",
        "https://compar.canaldelcongreso.gob.mx/Congreso/dist/images/451_big.png",
        "https://directostv.teleame.com/wp-content/uploads/2018/02/Canal-del-Congreso-Mexico-en-vivo-Online.png"
      ];

      
      
      
      
      const images14 = [
        "https://upload.wikimedia.org/wikipedia/commons/thumb/b/bc/TV_Excelsior.svg/1200px-TV_Excelsior.svg.png",
        "https://images-wixmp-ed30a86b8c4ca887773594c2.wixmp.com/f/4dff12f1-efa0-4572-ada1-cf3e8cc13ede/dfl8kla-9cc23c4a-98f4-4882-b628-ee3ac7e281ab.jpg/v1/fill/w_1280,h_961,q_75,strp/tv_excelsior__1974__vinheta_by_subwooferlabs_dfl8kla-fullview.jpg?token=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJ1cm46YXBwOjdlMGQxODg5ODIyNjQzNzNhNWYwZDQxNWVhMGQyNmUwIiwiaXNzIjoidXJuOmFwcDo3ZTBkMTg4OTgyMjY0MzczYTVmMGQ0MTVlYTBkMjZlMCIsIm9iaiI6W1t7ImhlaWdodCI6Ijw9OTYxIiwicGF0aCI6IlwvZlwvNGRmZjEyZjEtZWZhMC00NTcyLWFkYTEtY2YzZThjYzEzZWRlXC9kZmw4a2xhLTljYzIzYzRhLTk4ZjQtNDg4Mi1iNjI4LWVlM2FjN2UyODFhYi5qcGciLCJ3aWR0aCI6Ijw9MTI4MCJ9XV0sImF1ZCI6WyJ1cm46c2VydmljZTppbWFnZS5vcGVyYXRpb25zIl19.hoWl6QKdwD-qAfp22bV6GRs9MA7JwWunG26sEcy3sBA",
        "https://laotraopinion.s3.amazonaws.com/wp-content/uploads/2020/01/Exc%C3%A9lsior-TV.jpg?x58111",
        "https://i.ytimg.com/vi/ikQiLWdtAbE/maxresdefault.jpg"
      ];
      
      
      
      
      const images15 = [
        "https://pbs.twimg.com/profile_images/1116025020822634497/Pd-Rvw-k_400x400.jpg",
        "https://expresatv.com.mx/wp-content/uploads/2023/04/LLEGO-LA-HORA-DE-HABLAR.jpg",
        "https://expresatv.com.mx/wp-content/uploads/2023/04/expresa-600x200-1.png",
        "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQlg1FOnyigaco8wsAQhxifmuzjiL0MTX0uqA&usqp=CAU",
      ];

      
      
      
      const images16 = [
        "https://upload.wikimedia.org/wikipedia/commons/5/5c/Logo-ForoTV-2020.png",
        "https://images.squarespace-cdn.com/content/v1/5bb2ffa57a1fbd5c3246777a/1539288497348-1LBVO4SXNNN2WKEKANF8/IMAGE.jpg",
        "https://tvnotiblog.com/wp-content/uploads/2010/02/logo-forotv.jpg",
        "https://static.nmas.com.mx/nmas-news/styles/463x300/cloud-storage/wp-thumbnails/como-ver-foro-tv-en-vivo.png?itok=C5kOaWRg"
      ];

      
      
      
      
      const images17 = [
        "https://cdn.imagentv.com/resources/sin_envivo.jpg",
        "https://selectra.mx/sites/selectra.mx/files/styles/article_hero/public/images/imagen-tv-mx-825x293_0.png?itok=Lja04CCQ",
        "https://cdn.imagentv.com/resources/defaults/v2/imagen_default300.png",
        "https://brandemia.org/sites/default/files/sites/default/files/grupo_imagen_logo.jpg"
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







  const searchButton = document.getElementById('search-button');
  const searchInput = document.getElementById('search-bar');
  const cards = document.querySelectorAll('.card');

  searchButton.addEventListener('click', () => {
    const searchText = searchInput.value.toLowerCase();
    cards.forEach(card => {
      const imageSrc = card.querySelector('.card-img').getAttribute('src').toLowerCase();
      if (imageSrc.includes(searchText)) {
        card.style.display = 'block';
      } else {
        card.style.display = 'none';
      }
    });
  });









var modal = document.getElementById("myModal");
  var button = document.getElementById("myButton");
  var close = document.getElementsByClassName("close")[0];
  var distritocomedia = document.getElementById("distritocomedia");

  button.onclick = function() {
    modal.style.display = "block";
    distritocomedia.innerHTML = "<script type='text/javascript' src='https://www.televisiongratishd.com/embed.js'></script>";
  }

  close.onclick = function() {
    modal.style.display = "none";
  }

  window.onclick = function(event) {
    if (event.target == modal) {
      modal.style.display = "none";
    }
  }
