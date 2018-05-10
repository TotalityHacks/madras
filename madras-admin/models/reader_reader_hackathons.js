'use strict';

module.exports = (sequelize, DataTypes) => {
  var Model = sequelize.define('reader_reader_hackathons', {
  }, {
    tableName: 'reader_reader_hackathons',
    
    timestamps: false,
    schema: process.env.DATABASE_SCHEMA,
  });

  Model.associate = (models) => {
    Model.belongsTo(models.reader_reader, {
      foreignKey: 'reader_id',
      
      as: '_reader_id',
    });
    
    Model.belongsTo(models.director_hackathon, {
      foreignKey: 'hackathon_id',
      
      as: '_hackathon_id',
    });
    
  };

  return Model;
};

