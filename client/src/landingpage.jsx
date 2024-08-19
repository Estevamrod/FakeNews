import Navbar from "./components/Navbar"
import smartphone from './assets/smartphone.svg'
import elderly from './assets/elderly.svg'
import form_1 from './assets/form_1.svg'
import form_2 from './assets/form_2.svg'
import form_3 from './assets/form_3.svg'
import logo from './assets/logo.svg'
import cesar from './assets/cesar.jpg'
import estevam from './assets/estevam.jpeg'
import sergio from './assets/sergio.png'


function LandingPage(){
    return(
        <div>
            <Navbar/>
            <div className="">
                <div className="flex justify-center items-center text-center flex-col lg:flex-row">
                
                    <div className="lg:mr-[50px] flex items-center justify-center flex-col lg:ml-[130px] ml-[50px] mr-[50px]">
                        <img src={logo} alt="Logo Veracidade" className="w-[350px] lg:w-[300px] mb-[20px]"/>
                        <h1 className="font-black text-[25px] mr-[25px] ml-[25px] mt-[10px] lg:text-[35px] lg:mr-0 lg:ml-0">A <span className="text-blue-500">VERACIDADE DAS NOTÍCIAS</span> NA PALMA DA SUA MÃO</h1>
                        <p className="text-[18px] lg:text-[23px] m-0">Descubra se as notícias que você viu hoje realmente são reais ou apenas uma fake news.</p>
                        <a href="/">
                            <button className="bg-blue-500 font-black text-white rounded-[40px] mt-[20px] pr-[60px] pl-[60px] p-[20px] text-[17px] lg:mt-[20px] hover:bg-white hover:border-[1px] hover:border-blue-500 hover:text-blue-500 hover:p-[19px] hover:pl-[60px] hover:pr-[60px]">COMEÇAR</button>
                        </a>
                    </div>
                    <img src={smartphone} alt="smartphone" className="w-[500px] lg:w-[600px]" />
                </div>

            <div className="border-b border-gray-300 my-8 m-[25px]"></div>

            <div className="flex justify-center items-center text-center flex-col lg:flex-row lg:mt-[50px] lg:mb-[50px]">
                <div className="lg:ml-[130px] lg:mr-[30px] ">
                <h1 className="font-black text-blue-500 text-[25px] lg:text-[35px]">COMO ASSIM VERIFICAR FAKE NEWS?</h1>
                <p className="m-[25px] lg:text-[22px] text-justify text-[21px] mr-[30px] ml-[30px]">O Veracidade <span className="text-blue-500">não tem o objetivo de determinar o que é real ou falso,</span> mas sim de fornecer informações que ajudam o leitor a tirar suas próprias conclusões sobre a notícia.</p>
                </div>
                <img src={elderly} alt="idosa" className="w-[75%] lg:w-[500px] lg:mr-[130px]"/>
            </div>

            <div className="border-b border-gray-300 my-8 m-[25px]"></div>

            <div className="flex justify-center items-center text-center flex-col">
                <h1 className="font-black text-blue-500 text-[25px] lg:text-[25px] mt-[20px]">QUAIS SÃO AS FONTES DAS INFORMAÇÕES?</h1>
                <p className="m-[25px] text-[21px] mr-[70px] ml-[70px] lg:text-[23px]">Nossas principais <span className="text-blue-500">fontes de dados</span> são sites de notícias, como:</p>
                
                <div className="flex items-center justify-center flex-col lg:flex-row">
                <div className="flex justify-center items-center flex-col min-w-60 max-w-sm bg-white shadow-[0_8px_30px_rgb(0,0,0,0.12)] rounded-[30px] w-10 p-4 m-2">
                    <img src="https://lh3.googleusercontent.com/proxy/urrkiM40BWHTfqwyUki0JxBAkop4QcKaaA8li9T39HojUjWHanEfu68i--MW3SfPQcERexTuFCVpE5u5IyAJm2mkJWFB6hp16BSNfXwdE6SxSXi0ewLJ5HyZim_Qw4R4kepkcw" alt="G1" className="w-32 rounded-[30px]"/>
                    <button className="bg-blue-500 font-black text-white p-[10px] pr-[15px] pl-[15px] rounded-full m-[15px] hover:bg-white hover:border-[1px] hover:border-blue-500 hover:text-blue-500 hover:p-[9px] hover:pl-[14px] hover:pr-[14px]">Clique para acessar</button>
                </div>
            
                <div className="flex justify-center items-center flex-col min-w-60 max-w-sm bg-white shadow-[0_8px_30px_rgb(0,0,0,0.12)] rounded-[30px] w-10 p-4 m-2">
                    <img src="https://upload.wikimedia.org/wikipedia/commons/9/97/Gp_marca.jpg" alt="G1" className="w-32 rounded-[30px]"/>
                    <button className="bg-blue-500 font-black text-white p-[10px] pr-[15px] pl-[15px] rounded-full m-[15px] hover:bg-white hover:border-[1px] hover:border-blue-500 hover:text-blue-500 hover:p-[9px] hover:pl-[14px] hover:pr-[14px]">Clique para acessar</button>
                </div> 

                <div className="flex justify-center items-center flex-col min-w-60 max-w-sm bg-white shadow-[0_8px_30px_rgb(0,0,0,0.12)] rounded-[30px] w-10 p-4 m-2">
                    <img src="https://play-lh.googleusercontent.com/jFIwbIofKnamJhU4l5eOeRvf7Zy-VF7avOsUcTmsji9xtKR_Dc6CT7hR1siQkHHBX5w" alt="G1" className="w-32 rounded-[30px]"/>
                    <button className="bg-blue-500 font-black text-white p-[10px] pr-[15px] pl-[15px] rounded-full m-[15px] hover:bg-white hover:border-[1px] hover:border-blue-500 hover:text-blue-500 hover:p-[9px] hover:pl-[14px] hover:pr-[14px]">Clique para acessar</button>
                </div>
            
                <div className="flex justify-center items-center flex-col min-w-60 max-w-sm bg-white shadow-[0_8px_30px_rgb(0,0,0,0.12)] rounded-[30px] w-10 p-4 m-2">
                    <img src="https://upload.wikimedia.org/wikipedia/pt/3/32/Estadao_logo.png" alt="G1" className="w-32 rounded-[30px]"/>
                    <button className="bg-blue-500 font-black text-white p-[10px] pr-[15px] pl-[15px] rounded-full m-[15px] hover:bg-white hover:border-[1px] hover:border-blue-500 hover:text-blue-500 hover:p-[9px] hover:pl-[14px] hover:pr-[14px]">Clique para acessar</button>
                </div>
                </div>
            </div>
            
            <div className="border-b border-gray-300 my-8 m-[25px]"></div>
                
                <div className="flex items-center justify-center flex-col">
                    <h1 className="font-black text-blue-500 text-[25px] lg:text-[25px] m-[20px]">QUAIS INFORMAÇÕES SÃO APRESENTADAS?</h1>
                    <div className="lg:flex lg:items-center lg:justify-center lg:mr-[221px] lg:ml-[221px] mb-[20px]">
                        <img src={form_1} alt="Forma 1" className="hidden lg:flex lg:w-[90px]"/>
                        <p className="m-[25px] lg:text-[23px] text-justify text-[21px] ml-[70px] mr-[70px]">O <span className="text-blue-500 font-black">sentimento</span> reflete a <span className="text-blue-500">emoção expressa na notícia,</span> classificando-a como positiva, neutra ou negativa. Notícias excessivamente positivas podem ser sensacionalistas, enquanto notícias muito negativas tendem a ser pessimistas. O ideal é que a notícia seja neutra, evitando influenciar o leitor a tirar conclusões precipitadas.</p>
                    </div>
                    <div className="lg:flex lg:items-center lg:justify-center lg:mr-[221px] lg:ml-[221px] mb-[20px]">
                        <img src={form_2} alt="Forma 2" className="hidden lg:flex lg:w-[90px]"/>
                        <p className="m-[25px] lg:text-[23px] text-justify text-[21px] ml-[70px] mr-[70px]">A <span className="text-blue-500 font-black">data</span> associada à emoção <span className="text-blue-500">indica quando uma notícia semelhante à manchete pesquisada foi publicada.</span> Isso ajuda a determinar se o assunto é atual ou se é um tema antigo que voltou a ganhar relevância.</p>
                    </div>
                    <div className="lg:flex lg:items-center lg:justify-center lg:mr-[221px] lg:ml-[221px]">
                        <img src={form_3} alt="Forma 3" className="hidden lg:flex lg:w-[90px]"/>
                        <p className="m-[25px] lg:text-[23px] text-justify text-[21px] ml-[70px] mr-[70px]">A <span className="text-blue-500 font-black">similaridade</span> mostra a <span className="text-blue-500">porcentagem de semelhança entre a manchete pesquisada e outras notícias.</span> Também são exibidas as <span className="text-blue-500">manchetes e subtítulos das notícias, além dos links</span> para que o leitor possa acessar o conteúdo completo nos sites oficiais.</p>
                    </div>
                </div>

                <div className="border-b border-gray-300 my-8 m-[25px]"></div>

                <div className="flex flex-col items-center justify-center">
                    <h1 className="font-black text-blue-500 lg:text-[25px] m-[20px] text-[25px]">QUEM SOMOS?</h1>
                    <div className="lg:flex">
                        <div className="flex flex-col items-center justify-center">
                            <img src={cesar} alt="Imagem César" className="rounded-full w-[250px] m-[25px] "/>
                            <p className="underline decoration-solid text-blue-500 font-bold lg:text-[18px] text-[17px]"><a href="https://www.linkedin.com/in/c%C3%A9sar-teodoro-5032ba283/">César Alexandre Teodoro</a></p>
                        </div>
                        <div className="flex flex-col items-center justify-center">
                            <img src={estevam} alt="Imagem César" className="rounded-full w-[250px] m-[25px] "/>
                            <p className="underline decoration-solid text-blue-500 font-bold lg:text-[18px] text-[17px]"><a href="https://www.linkedin.com/in/estevam-otavio-672b13265/">Estevam Otavio Rodrigues</a></p>
                        </div>
                        <div className="flex flex-col items-center justify-center">
                            <img src={sergio} alt="Imagem César" className="rounded-full w-[250px] m-[25px] "/>
                            <p className="underline decoration-solid text-blue-500 font-bold lg:text-[18px] text-[17px]"><a href="https://www.instagram.com/biologiacomsergio?utm_source=ig_web_button_share_sheet&igsh=ZDNlZDc0MzIxNw==">Sérgio Eduardo Cândido</a></p>
                        </div>
                    </div>
                    <p className="m-[25px] lg:mr-[221px] lg:ml-[221px] lg:text-[23px] mt-[30px] text-justify text-[21px] mr-[70px] ml-[70px]">Somos professores e alunos da Escola Estadual Deputado Salim Sedeh. Participam do projeto César Alexandre Teodoro e Estevam Otávio Rodrigues, estudantes do curso técnico de Desenvolvimento de Sistemas, e Sérgio Eduardo Cândido, professor de Biologia. A ideia do projeto foi inicialmente proposta pelo professor Sérgio, e os alunos adaptaram a ideia para torná-la aplicável e escalável, utilizando nossos conhecimentos em programação e design. Após um longo período de desenvolvimento, que incluiu várias fases de pesquisa e produção, focamos em entregar o melhor produto final para nossos usuários. Embora ainda tenhamos muitas ideias para implementar no futuro, estamos satisfeitos com o progresso e os resultados alcançados até agora.</p>
                </div>
                
                <div className="bg-blue-500 w-[100%] h-[30px] mt-[20px]"></div>
            </div>
        </div>
    )
}

export default LandingPage